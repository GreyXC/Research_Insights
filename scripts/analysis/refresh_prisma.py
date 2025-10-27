import subprocess

def refresh_prisma():
    subprocess.run(["python", "-m", "scripts.clean.clean_data"], check=True)
    subprocess.run(["python", "-m", "scripts.analysis.count_prisma_stages"], check=True)
    subprocess.run(["python", "-m", "scripts.analysis.generate_prisma_csv"], check=True)