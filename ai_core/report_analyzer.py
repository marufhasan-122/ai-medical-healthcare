NORMAL_RANGES = {
    "hemoglobin": (12, 17),
    "wbc": (4000, 11000),
    "fasting_glucose": (70, 100),
    "platelets": (150000, 450000)
}

def analyze_report(report):
    findings = []
    for test, value in report.items():
        low, high = NORMAL_RANGES.get(test, (None, None))
        if low and value < low:
            findings.append(f"{test} LOW → Possible anemia/infection")
        elif high and value > high:
            findings.append(f"{test} HIGH → Possible risk")
        else:
            findings.append(f"{test} NORMAL")
    return findings
