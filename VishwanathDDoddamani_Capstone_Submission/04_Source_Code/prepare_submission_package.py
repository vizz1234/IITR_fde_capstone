"""
Helper script to package the project into the required 4-folder submission layout:
  01_Video/
  02_Report/
  03_Workbooks/
  04_Source_Code/

Usage: python prepare_submission_package.py --name YourName
Example: python prepare_submission_package.py --name PriyaSharma
"""

import os
import shutil
import argparse


def package_submission(user_name: str):
    user_name_clean = user_name.replace(" ", "")
    base_dir = os.path.abspath(os.path.dirname(__file__))
    dist_dir = os.path.join(base_dir, f"{user_name_clean}_Capstone_Submission")

    print(f"Packaging submission for '{user_name_clean}' into: {dist_dir}")

    # Remove old staging dir if exists
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    # Create top-level submission folders
    folder_video = os.path.join(dist_dir, "01_Video")
    folder_report = os.path.join(dist_dir, "02_Report")
    folder_workbooks = os.path.join(dist_dir, "03_Workbooks")
    folder_code = os.path.join(dist_dir, "04_Source_Code")

    os.makedirs(folder_video, exist_ok=True)
    os.makedirs(folder_report, exist_ok=True)
    os.makedirs(folder_workbooks, exist_ok=True)
    os.makedirs(folder_code, exist_ok=True)

    # 1. 01_Video placeholder readme
    with open(os.path.join(folder_video, "README_VIDEO_INSTRUCTIONS.txt"), "w") as f:
        f.write(f"Place your recorded ~20-minute video here as '{user_name_clean}_Capstone_Video.mp4' or paste your video link in a text file.\n")

    # 2. 02_Report
    report_src = os.path.join(base_dir, "docs", "Capstone_Project_Report.md")
    if os.path.exists(report_src):
        shutil.copy(report_src, os.path.join(folder_report, f"{user_name_clean}_Capstone_Report.md"))
    pdf_report_src = os.path.join(base_dir, "docs", "Capstone Project Report — CloudServe AI Support System _ IIT Roorkee FDE.pdf")
    if os.path.exists(pdf_report_src):
        shutil.copy(pdf_report_src, os.path.join(folder_report, f"{user_name_clean}_Capstone_Report.pdf"))

    # 3. 03_Workbooks
    docs_dir = os.path.join(base_dir, "docs")
    if os.path.exists(docs_dir):
        for item in os.listdir(docs_dir):
            if item.endswith(".md") or item.endswith(".pdf"):
                shutil.copy(os.path.join(docs_dir, item), os.path.join(folder_workbooks, item))

    # Also copy Effort_Log as PDF/MD named FirstnameLastname_Effort_Log.md
    effort_log_src = os.path.join(docs_dir, "Effort_Log.md")
    if os.path.exists(effort_log_src):
        shutil.copy(effort_log_src, os.path.join(folder_workbooks, f"{user_name_clean}_Effort_Log.md"))
    effort_pdf_src = os.path.join(base_dir, "docs", "Effort Log — Vishwanath D Doddamani _ FDE Capstone.pdf")
    if os.path.exists(effort_pdf_src):
        shutil.copy(effort_pdf_src, os.path.join(folder_workbooks, f"{user_name_clean}_Effort_Log.pdf"))

    # 4. 04_Source_Code
    # Copy source code files while excluding secrets (.env), storage, .venv, etc.
    ignore_func = shutil.ignore_patterns(
        ".env", ".venv", "venv", "__pycache__", ".pytest_cache",
        "*.db", "*.sqlite", "storage", ".git", f"{user_name_clean}_Capstone_Submission*", "*.zip"
    )

    for item in os.listdir(base_dir):
        if item in [f"{user_name_clean}_Capstone_Submission"]:
            continue
        src_path = os.path.join(base_dir, item)
        dst_path = os.path.join(folder_code, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, ignore=ignore_func)
        else:
            if not item.endswith(".env") and not item.endswith(".zip"):
                shutil.copy(src_path, dst_path)

    # Create zip archive
    zip_path = shutil.make_archive(dist_dir, "zip", dist_dir)
    print(f"\nSUCCESS! Submission package created:")
    print(f"  Zip Archive: {zip_path}")
    print(f"  Folder Structure:\n    01_Video/\n    02_Report/\n    03_Workbooks/\n    04_Source_Code/\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package Capstone Submission Archive")
    parser.add_argument("--name", type=str, default="Student_Submission", help="Your full name (e.g., PriyaSharma)")
    args = parser.parse_args()

    package_submission(args.name)
