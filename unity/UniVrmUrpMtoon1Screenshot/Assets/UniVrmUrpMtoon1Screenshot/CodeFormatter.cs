using System.Diagnostics;
using UnityEditor;

namespace UniVrmUrpMtoon1Screenshot
{
    public class CodeFormatter : AssetPostprocessor
    {
        void OnPreprocessAsset()
        {
            if (!assetPath.StartsWith("Assets/") || !assetPath.EndsWith(".cs"))
            {
                return;
            }

            UnityEngine.Debug.LogFormat("IMPORT: {0}", assetPath);

            using var process = Process.Start(
                new ProcessStartInfo
                {
                    FileName = "dotnet",
                    ArgumentList = { "csharpier", assetPath },
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                }
            );
        }
    }
}
