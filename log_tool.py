import argparse
from collections import Counter
import os
from colorama import Fore, init
import requests

init(autoreset=True)

def explain_top_error_with_gemma(error_type):
    prompt = f"What does the error '{error_type}' typically mean in a backend system, and how might one troubleshoot it ?"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json = {
                "model" : "gemma:2b",
                "prompt" : prompt,
                "stream" : False
            }
        )
        data = response.json()
        return data.get("response", "⚠️ No response from Gemma.")
    except Exception as e:
        return f"⚠️ Failed to connect to local LLM: {e}"


def parse_logs(filepath):
    errors = []
    warnings = []
    all_logs = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            all_logs.append(line)

            if "ERROR" in line:
                errors.append(line)
            elif "WARN" in line:
                warnings.append(line)

    return all_logs, errors, warnings


def summarize_logs(errors, warnings):
    error_types = Counter()
    warn_types = Counter()

    for e in errors:
        try:
            err_type = e.split("ERROR")[1].strip().split(":")[0]
            error_types[err_type] += 1
        except IndexError:
            error_types["Unknown"] += 1

    for w in warnings:
        try:
            warn_type = w.split("WARN")[1].strip().split(":")[0]
            warn_types[warn_type] += 1
        except IndexError:
            warn_types["Unknown"] += 1

    return error_types, warn_types


def generate_report(filepath, all_logs, errors, warnings, error_types, warn_types):
    with open(filepath, "w") as f:
        f.write("===== Log Summary Report =====\n\n")
        f.write(f"Total log lines: {len(all_logs)}\n")
        f.write(f"Total errors: {len(errors)}\n")
        f.write(f"Total warnings: {len(warnings)}\n\n")

        f.write("Error Types:\n")
        for et, count in error_types.items():
            f.write(f" - {et}: {count}\n")
        f.write("\n")

        f.write("Warning Types:\n")
        for wt, count in warn_types.items():
            f.write(f" - {wt}: {count}\n")
        f.write("\n")

        f.write("Recent Errors:\n")
        for e in errors[-5:]:
            f.write(f" - {e}\n")

        f.write("\n===== End of Report =====\n")

        if error_types:
            top_error = error_types.most_common(1)[0][0]
            explanation = explain_top_error_with_gemma(top_error)
            f.write(f"\nGemma Insight for '{top_error}':\n")
            f.write(f"{explanation}\n")


def main():
    parser = argparse.ArgumentParser(description="Simple Log Diagnostic Tool")
    parser.add_argument('--preview', action='store_true', help='Print recent logs to screen with colors')
    parser.add_argument("--log", type=str, required=True, help="Path to log file")
    parser.add_argument("--summary", type=str, default="report/summary.txt", help="Path to summary output file")

    args = parser.parse_args()

    all_logs, errors, warnings = parse_logs(args.log)
    error_types, warn_types = summarize_logs(errors, warnings)

    if args.preview:
        print(Fore.CYAN + "\nRecent Errors:")
        for e in errors[-5:]:
            print(Fore.RED + " - " + e)

    os.makedirs(os.path.dirname(args.summary), exist_ok=True)
    generate_report(args.summary, all_logs, errors, warnings, error_types, warn_types)

    print(Fore.GREEN + f"\n✅ Summary written to {args.summary}")





if __name__ == "__main__":
    main()
