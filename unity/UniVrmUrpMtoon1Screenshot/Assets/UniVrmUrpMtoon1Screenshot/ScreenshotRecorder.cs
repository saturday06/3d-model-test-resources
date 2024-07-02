using System;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace UniVrmUrpMtoon1Screenshot
{
    public static class ScreenshotRecorder
    {
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
        private static void Start()
        {
            Debug.Log("Start");

            if (SceneManager.GetActiveScene().name.Length > 0)
            {
                return;
            }

            var sceneName = "Sphere1";
            SceneManager.LoadScene(sceneName, LoadSceneMode.Additive);
            Task.Delay(TimeSpan.FromSeconds(10))
                .ContinueWith(
                    _ =>
                    {
                        SceneManager.UnloadSceneAsync(sceneName);
                    },
                    CancellationToken.None,
                    TaskContinuationOptions.None,
                    TaskScheduler.FromCurrentSynchronizationContext()
                );
        }
    }
}
