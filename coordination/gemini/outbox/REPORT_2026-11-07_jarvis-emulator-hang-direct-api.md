# Gemini engineering report

- Task file: coordination/gemini/dispatch/2026-11-07_jarvis-emulator-hang-direct-api.md
- Model: gemini-3.8-flash
- Generated: 2026-11-07 06:54:03 UTC
- Source: direct Gemini Developer API

# Engineering Diagnosis: Android Emulator Hangs in CI Smoke Tests (`sokfrut-tech/Gemeni`)

**Date:** 2026-11-07  
**System:** GitHub Actions (`ubuntu-latest` / Ubuntu 24.04), Android Emulator API 34  
**Author:** Gemini (Senior Engineering Agent)  
**Status:** Independent Diagnostic Report  

---

## 1. Verified Facts vs. Hypotheses

To avoid false assumptions during root-cause analysis, system observations are categorized into confirmed empirical data and unverified hypotheses.

### A. Verified Facts (Empirical Evidence)
1. **Job Hangs:** Four separate workflow runs across distinct branches (`Run 42347172763`, `Run 42346984667`, `Run 42346510482`, `Run 42346830463`) hung in the step `Run Android emulator smoke tests`.
2. **Prior Steps Succeeded:** Upstream setup stages (checkout, JDK 17, Gradle 8.9 wrapper setup, CodeQL/security checks) completed successfully in all four runs before the emulator step was entered.
3. **Log Unavailability:** Live GitHub Actions logs returned `BlobNotFound` during active runs; no per-line stdout/stderr was persisted or flushed to GitHub’s log endpoint prior to step termination.
4. **Configuration Parameters:**
   - Base image: `ubuntu-latest` (Ubuntu 24.04 LTS).
   - Target image: `system-images;android-34;google_apis;x86_64`.
   - Emulator flags: `-no-window -gpu swiftshader_indirect -no-snapshot -noaudio -no-boot-anim -camera-back none`.
   - Configured boot timeout inside action: 900 seconds (15 minutes).
   - Step/Action execution timeout: 32 minutes.
   - Overall job timeout: 35 minutes.
   - Command executed: `./gradlew --no-daemon :app:connectedDebugAndroidTest`.
5. **Post-Mortem Execution Failure:** Post-step failure diagnostics and artifact uploads did not execute because the action step never completed before the job timed out or stalled.

### B. Hypotheses (Requiring Direct Log Validation)
1. **Boot Loop vs. Cold Boot Stalling:** The emulator may have exhausted its 900-second internal boot check, or the wrapper action failed to recognize `sys.boot_completed=1` despite Android starting.
2. **Software GPU / CPU Throttling:** `swiftshader_indirect` on standard 2-core / 4-core GitHub-hosted Linux runners can cause software rendering overhead that starves ADB daemon keepalives.
3. **Gradle Instrumentation Deadlock:** The emulator may have booted cleanly, but `:app:connectedDebugAndroidTest` deadlocked during APK install, instrumentation handshake, test runner initialization, or an unhandled UI thread freeze.
4. **Action Wrapper Deadlock:** The third-party composite/JavaScript action running the emulator (`reactivecircus/android-emulator-runner` or equivalent) may have hung in a subshell or child process pipeline without propagating exit signals.

---

## 2. Ranked Root Cause Analysis

| Rank | Likely Cause Category | Confidence | Evidence & Failure Mechanics |
| :--- | :--- | :--- | :--- |
| **1** | **Emulator Boot Stalling / Software Rendering Starvation (`swiftshader_indirect` + nested KVM)** | **High** (80%) | Running API 34 `google_apis` on `ubuntu-24.04` under software rasterization (`swiftshader_indirect`) is notoriously heavy. When Google APIs play services start alongside boot services on constrained virtual CPUs, system load spikes, leading to ADB connection drops (`Broken pipe`), IPC timeouts, and boot timeouts exceeding 15 minutes. |
| **2** | **Action Wrapper Blocking / Uncaught Subshell Failure** | **Medium-High** (75%) | The action wrapper runs the boot monitor and Gradle script in a shared lifecycle. If the emulator daemon forks or writes unbuffered data to standard streams that block on an unread pipe, the runner process stalls indefinitely until the step's 32-minute timeout triggers. |
| **3** | **Gradle Connected Test Deadlock / ANR during Instrumentation Setup** | **Medium** (60%) | If the emulator finishes booting, `connectedDebugAndroidTest` takes over. If the test runner encounters an unhandled runtime permission prompt, an uncaught main-thread exception during native asset loading, or an unresponsive test harness, `am instrument` blocks without timing out unless `android.testOptions` specifies an execution timeout. |
| **4** | **ADB Server State Desynchronization (`adb server killed` / Socket Hanging)** | **Medium** (55%) | Ubuntu 24.04 runner environments have updated kernel/glibc configurations. Rapid spawning of `adb` commands against a QEMU instance experiencing high CPU load often causes `adb server` socket disconnections or freezes where `adb` hangs on `wait-for-device`. |
| **5** | **Runner Resource / I/O Saturation** | **Low-Medium** (40%) | Standard GitHub-hosted `ubuntu-latest` instances provide 2 vCPUs (or 4 vCPUs on specific enterprise allocations) and 7–14 GB RAM. An API 34 AVD requesting 4 cores and a large RAM allocation forces swap trashing and high I/O wait, causing extreme slowdowns without an explicit crash. |
| **6** | **Cross-Job Concurrency Contention** | **Low** (10%) | Independent GitHub-hosted workflow runs execute on completely isolated virtual machines. Concurrency between runs does not cause shared CPU/RAM resource starvation on GitHub's infrastructure. |

---

## 3. The 32-Minute Action vs. 35-Minute Job Timeout Paradox

The current workflow configuration creates an operational blind spot due to nested timeout mechanics:

```
[Job Start] (0m)
   │
   ├─► Setup / Checkout / JDK (e.g., 2m)
   │
   ├─► Step: Run Android emulator smoke tests (timeout-minutes: 32)
   │     │
   │     ├─► Emulator launch / Gradle execution (Hangs here)
   │     │
   │     └─► [32m Step Timeout Reached] (Absolute Job Time: 34m)
   │
   ├─► Step: Collect Diagnostics (`if: failure()`)
   │     └─► Requires 1–3 minutes to collect logs, dump logcat, and upload
   │
   └─► [35m Job Timeout Hard Kill] ──► Runner kills process immediately via SIGKILL
```

### Why Diagnostics Never Run:
1. **Sequential Timeout Collision:** If the smoke test step hits its 32-minute action timeout at `T = 34 minutes` (after 2 minutes of setup), the GitHub Actions runner attempts to clean up the step and transition to the next step.
2. **Missing `always()` Guard:** If the diagnostic step is configured with `if: failure()`, but the step timeout cancellation sets the job status to `cancelled` rather than `failure`, the diagnostic step is skipped entirely unless configured with `if: always()` or `if: cancelled() || if: failure()`.
3. **Buffer Eviction under Hard Termination:** Even if triggered at minute 34, the runner hits the global `timeout-minutes: 35` hard boundary within 60 seconds. The GitHub runner terminates all processes (`SIGKILL`), tearing down the VM before diagnostic logs can be collected or uploaded to GitHub artifact storage.

---

## 4. Concrete Minimal YAML / Workflow Remediation

To guarantee visibility and bound execution times, replace the black-box runner execution with an instrumented, phased shell sequence. The job must allocate explicit budgets:
- **Emulator boot:** 8 minutes.
- **Test execution:** 7 minutes.
- **Diagnostics & artifact capture:** 5 minutes.
- **Job timeout:** 25 minutes total.

```yaml
    name: Run Android Smoke Tests
    runs-on: ubuntu-latest
    timeout-minutes: 25

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Android SDK Tools
        uses: android-actions/setup-android@v3

      - name: Enable Hardware Acceleration / KVM Check
        run: |
          echo "[$(date -u +%T)] Verifying KVM availability..."
          if [ -e /dev/kvm ] && [ -w /dev/kvm ]; then
            echo "KVM acceleration is available."
          else
            echo "WARNING: /dev/kvm is not writable. Software fallback will degrade performance."
          fi

      - name: Create and Launch Emulator
        run: |
          echo "[$(date -u +%T)] Installing AVD system image..."
          echo "y" | sdkmanager "system-images;android-34;google_apis;x86_64" "platforms;android-34" > /dev/null

          echo "[$(date -u +%T)] Creating AVD..."
          echo "no" | avdmanager create avd -n test_avd -k "system-images;android-34;google_apis;x86_64" --force --device "pixel"

          echo "[$(date -u +%T)] Starting emulator daemon..."
          $ANDROID_HOME/emulator/emulator -avd test_avd \
            -no-window \
            -gpu swiftshader_indirect \
            -no-snapshot \
            -noaudio \
            -no-boot-anim \
            -camera-back none \
            -camera-front none \
            -timezone UTC \
            -memory 3072 \
            -cores 2 &
          EMU_PID=$!
          echo "EMULATOR_PID=$EMU_PID" >> $GITHUB_ENV

          echo "[$(date -u +%T)] Waiting for ADB server..."
          adb start-server
          adb wait-for-device

          echo "[$(date -u +%T)] Device connected. Polling boot completion..."
          BOOT_TIMEOUT=480
          ELAPSED=0
          BOOT_SUCCESS=0

          while [ $ELAPSED -lt $BOOT_TIMEOUT ]; do
            SYS_BOOT=$(adb shell getprop sys.boot_completed 2>/dev/null || echo "0")
            BOOT_ANIM=$(adb shell getprop init.svc.bootanim 2>/dev/null || echo "running")

            if [ "${SYS_BOOT//[$'\t\r\n']}" = "1" ] && [ "${BOOT_ANIM//[$'\t\r\n']}" = "stopped" ]; then
              echo "[$(date -u +%T)] Boot complete verified in ${ELAPSED}s."
              BOOT_SUCCESS=1
              break
            fi

            echo "[$(date -u +%T)] Booting... (Elapsed: ${ELAPSED}s, sys.boot_completed=${SYS_BOOT}, init.svc.bootanim=${BOOT_ANIM})"
            sleep 10
            ELAPSED=$((ELAPSED + 10))
          done

          if [ $BOOT_SUCCESS -ne 1 ]; then
            echo "[$(date -u +%T)] ERROR: Emulator failed to boot within ${BOOT_TIMEOUT}s."
            exit 1
          fi

          echo "[$(date -u +%T)] Dismissing initial keyguard and system UI dialogs..."
          adb shell input keyevent 82 || true
          adb shell settings put global window_animation_scale 0.0 || true
          adb shell settings put global transition_animation_scale 0.0 || true
          adb shell settings put global animator_duration_scale 0.0 || true

      - name: Run Connected Tests (Bounded Timeout)
        run: |
          echo "[$(date -u +%T)] Executing connected Android tests..."
          timeout 420s ./gradlew --no-daemon :app:connectedDebugAndroidTest \
            -Pandroid.testInstrumentationRunnerArguments.class=com.sokfrut.gemeni.SmokeTestSuite \
            --info
        env:
          GRADLE_OPTS: "-Dorg.gradle.daemon=false -Dorg.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m"

      - name: Capture Forensic Diagnostics
        if: always()
        run: |
          mkdir -p diagnostics-output
          echo "=== Timestamp: $(date -u) ===" > diagnostics-output/summary.txt
          echo "=== ADB Device State ===" >> diagnostics-output/summary.txt
          adb devices -l >> diagnostics-output/summary.txt 2>&1 || true

          echo "=== Emulator Process Info ===" >> diagnostics-output/summary.txt
          ps aux | grep emulator >> diagnostics-output/summary.txt 2>&1 || true

          echo "=== Dumping Logcat ==="
          adb logcat -d -v threadtime > diagnostics-output/logcat.txt 2>&1 || true

          echo "=== System Boot Properties ===" >> diagnostics-output/summary.txt
          adb shell getprop >> diagnostics-output/getprop.txt 2>&1 || true

          echo "=== Kernel DMESG (if permitted) ==="
          adb shell dmesg > diagnostics-output/dmesg.txt 2>&1 || true

          echo "=== Memory Info ===" >> diagnostics-output/summary.txt
          adb shell dumpsys meminfo >> diagnostics-output/dumpsys_meminfo.txt 2>&1 || true

      - name: Upload Diagnostics Artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: emulator-diagnostics-${{ github.run_id }}
          path: diagnostics-output/
          retention-days: 7
```

---

## 5. Controlled Experiment Matrix

To prevent compounding variables, test configuration changes in strict isolation while keeping the image pinned to `API 34, x86_64`.

| Experiment ID | Varied Factor | Baseline Value | Experimental Value | Evaluation Metric |
| :--- | :--- | :--- | :--- | :--- |
| **EXP-01** | **Instrumentation Observability** | Opaque wrapper action | Phased shell script + explicit boot polling + `if: always()` log dumping | Proves whether the stall is at Emulator Boot, Gradle compile, APK install, or Test execution. |
| **EXP-02** | **Graphics Renderer** | `-gpu swiftshader_indirect` | `-gpu host` (if KVM active) or `-gpu guest` | Measures boot time differences and CPU load; checks if `swiftshader` was locking the CPU. |
| **EXP-03** | **Virtual Core Allocation** | `-cores 4` | `-cores 2` | On 2-vCPU runner VMs, setting `-cores 4` induces severe context-switching overhead. Reducing to 2 cores often speeds up execution. |
| **EXP-04** | **System Image Target** | `google_apis` (API 34) | `default` (API 34 without Google Play/APIs) | Eliminates background initialization of Google Play Services, saving up to 50% CPU/RAM during boot. |
| **EXP-05** | **Test Target Scope** | `:app:connectedDebugAndroidTest` (Entire test suite) | Single minimal Smoke Test class (`SmokeTestSuite`) | Isolates whether an individual instrumentation test or native library is freezing the UI thread. |

---

## 6. Concurrency & Infrastructure Evaluation

### Concurrency Assessment:
- **Runner Model:** GitHub Actions runs each parallel job in an isolated, dedicated Microsoft Azure Virtual Machine. 
- **Resource Independence:** Parallel branches running jobs simultaneously do **not** share RAM, disk I/O, or vCPU allocations. Job 128328589043 cannot steal memory from Job 128328076036.
- **API Rate Limiting Considerations:** The only shared vector between separate jobs is network egress to Maven Central, Google Maven repository, or GitHub API rate limits. These steps completed successfully prior to the emulator launch.
- **Recommendation:** Do not throttle workflow concurrency. Restricting concurrency will slow down engineering throughput without resolving the underlying emulator boot/runner lockup.

---

## 7. Retry Strategy Guidance

### Why Blind Retries Must Be Avoided:
Applying generic retry mechanisms (e.g., `nick-fields/retry@v3` or wrapping steps in `retry: 3`) directly onto a 30-minute failing task is counterproductive:
1. It multiplies runner queue occupancy and CI minute consumption ($3 \times 32\text{ min} = 96\text{ min}$).
2. If the failure is deterministic (e.g., hypervisor incompatibility, missing KVM access, or CPU starvation under `swiftshader_indirect`), retries will fail at a 100% rate.

### Permissible Targeted Retries (Transient Conditions Only):
A retry is acceptable **only** for isolated, transient socket-level operations:
- Transient failure to download SDK system images from Google's CDN.
- An ADB server crash during daemon spin-up (`adb kill-server && adb start-server`).
- A single bounded retry for emulator cold-boot **only if** the first attempt times out at 300 seconds, and the retry is preceded by killing the stalled emulator process and purging the temporary AVD directory.

---

## 8. Scope of Action: Workflow Instrumentation vs. App Code

### Immediate Boundary: Workflow Instrumentation First
At this juncture, **no application source code changes (`/app/src/...`) are warranted or supported by the available data**.

1. **Lack of Pinpointed Evidence:** Because the workflow hung prior to log offloading, there is no evidence indicating an app-level crash, uncaught exception, or deadlock in Jarvis TTS/Qwen components.
2. **First Milestone:** The workflow must be modified with explicit step bounds, granular timestamp logging, and unconditional post-action diagnostics (`if: always()`).
3. **Trigger for Source Code Action:** Only if forensic diagnostics from EXP-01 reveal that `sys.boot_completed=1` was achieved and the test process (`am instrument`) stalled inside a specific application class (e.g., `JarvisApp.onCreate`, TTS initialization queue, or native Qwen asset extraction) should app-level remediation PRs be opened.
