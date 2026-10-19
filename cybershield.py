"""CyberShield Password Security Analyzer
A local educational tool. It never saves or sends the password anywhere.
"""

import re
import tkinter as tk
from tkinter import ttk


def analyze_password(password: str) -> tuple[int, list[str]]:
    """Return a simple educational score (0-100) and improvement tips."""
    if not password:
        return 0, ["Type a sample password to see its strength analysis."]

    score = 0
    tips = []

    if len(password) >= 8:
        score += 20
    else:
        tips.append("Use at least 8 characters; a longer passphrase is better.")

    if len(password) >= 12:
        score += 15
    if len(password) >= 16:
        score += 10

    checks = [
        (r"[a-z]", "Add lowercase letters if appropriate."),
        (r"[A-Z]", "Add uppercase letters if appropriate."),
        (r"\d", "Include numbers if useful."),
        (r"[^A-Za-z0-9]", "Consider punctuation or spaces."),
    ]
    for pattern, tip in checks:
        if re.search(pattern, password):
            score += 10
        else:
            tips.append(tip)

    # Repetition and common patterns reduce the educational score.
    if re.search(r"(.)\1{2,}", password):
        score -= 15
        tips.append("Avoid repeating the same character several times.")

    lowered = password.lower()
    common_fragments = ("password", "qwerty", "letmein", "admin", "welcome", "123456")
    if any(fragment in lowered for fragment in common_fragments):
        score -= 25
        tips.append("Avoid common words and predictable sequences.")

    if len(set(password)) <= 3 and len(password) >= 6:
        score -= 15
        tips.append("Use a more varied passphrase.")

    score = max(0, min(100, score))
    if not tips:
        tips.append("Good result for these basic checks. A unique passphrase is still important.")
    return score, tips


class CyberShieldApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("CyberShield | Password Security Analyzer")
        root.geometry("760x560")
        root.minsize(650, 500)
        root.configure(bg="#0b1220")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=9)
        style.configure("TLabel", background="#111c2f", foreground="#e5eefb", font=("Segoe UI", 10))
        style.configure("TProgressbar", troughcolor="#26364e", background="#22c55e")

        outer = tk.Frame(root, bg="#0b1220", padx=24, pady=22)
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer, text="CYBERSHIELD", bg="#0b1220", fg="#38bdf8",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")
        tk.Label(
            outer, text="Password Security Analyzer • Local-only educational tool",
            bg="#0b1220", fg="#9fb1ca", font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 18))

        card = tk.Frame(outer, bg="#111c2f", padx=18, pady=18)
        card.pack(fill="x")

        tk.Label(
            card, text="Enter a SAMPLE password to analyze",
            bg="#111c2f", fg="#e5eefb", font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            card, textvariable=self.password_var, show="•",
            bg="#07101e", fg="#f8fafc", insertbackground="#ffffff",
            relief="flat", font=("Consolas", 14), highlightthickness=1,
            highlightbackground="#334155", highlightcolor="#38bdf8"
        )
        self.password_entry.pack(fill="x", pady=(10, 12), ipady=9)
        self.password_entry.bind("<Return>", lambda _event: self.run_analysis())

        row = tk.Frame(card, bg="#111c2f")
        row.pack(fill="x")
        ttk.Button(row, text="Analyze", command=self.run_analysis).pack(side="left")
        ttk.Button(row, text="Clear", command=self.clear).pack(side="left", padx=8)
        self.show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            row, text="Show sample", variable=self.show_var, command=self.toggle_visibility,
            bg="#111c2f", fg="#cbd5e1", selectcolor="#07101e",
            activebackground="#111c2f", activeforeground="#ffffff"
        ).pack(side="left", padx=6)

        result = tk.Frame(outer, bg="#111c2f", padx=18, pady=18)
        result.pack(fill="both", expand=True, pady=(16, 0))
        tk.Label(
            result, text="Analysis result", bg="#111c2f", fg="#e5eefb",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        self.score_label = tk.Label(
            result, text="Score: —", bg="#111c2f", fg="#38bdf8",
            font=("Segoe UI", 16, "bold")
        )
        self.score_label.pack(anchor="w", pady=(10, 6))

        self.progress = ttk.Progressbar(result, maximum=100, mode="determinate")
        self.progress.pack(fill="x", pady=(0, 12))

        self.tips = tk.Text(
            result, height=7, wrap="word", bg="#07101e", fg="#dbeafe",
            insertbackground="#ffffff", relief="flat", font=("Segoe UI", 10),
            padx=10, pady=10
        )
        self.tips.pack(fill="both", expand=True)
        self.tips.insert("1.0", "Your analysis will appear here.\n")
        self.tips.configure(state="disabled")

        tk.Label(
            outer,
            text="Privacy: analysis happens on this computer. The app does not store or transmit input.",
            bg="#0b1220", fg="#86a3c2", font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(12, 0))

    def toggle_visibility(self) -> None:
        self.password_entry.configure(show="" if self.show_var.get() else "•")

    def run_analysis(self) -> None:
        password = self.password_var.get()
        score, tips = analyze_password(password)
        if score >= 75:
            label = "Stronger pattern"
        elif score >= 45:
            label = "Moderate pattern"
        else:
            label = "Weak pattern"
        self.score_label.configure(text=f"Score: {score}/100 — {label}")
        self.progress["value"] = score
        self.tips.configure(state="normal")
        self.tips.delete("1.0", "end")
        self.tips.insert("1.0", "\n".join(f"• {tip}" for tip in tips))
        self.tips.configure(state="disabled")

    def clear(self) -> None:
        self.password_var.set("")
        self.score_label.configure(text="Score: —")
        self.progress["value"] = 0
        self.tips.configure(state="normal")
        self.tips.delete("1.0", "end")
        self.tips.insert("1.0", "Your analysis will appear here.\n")
        self.tips.configure(state="disabled")
        self.password_entry.focus_set()


def main() -> None:
    root = tk.Tk()
    CyberShieldApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
