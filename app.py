#!/usr/bin/env python3
import os, sys, threading
from pathlib import Path

# Load .env
_env = Path(__file__).parent / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

import customtkinter as ctk
from generator import (
    generate_script, generate_caption, generate_ideas,
    generate_thumbnail_concept, generate_full_package,
    ContentRequest, ContentType, Platform,
)
from generator.saver import save_content, save_package

# ── Theme ──────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BRAND   = "#4CAF50"
BRAND2  = "#2E7D32"
BG      = "#0f1410"
CARD    = "#1a2118"
CARD2   = "#212e20"
TEXT    = "#e8f5e2"
MUTED   = "#7a9a72"
ACCENT  = "#66BB6A"

PLATFORM_MAP = {
    "YouTube":   Platform.YOUTUBE,
    "Instagram": Platform.INSTAGRAM,
    "TikTok":    Platform.TIKTOK,
    "Twitter":   Platform.TWITTER,
}

TYPE_MAP = {
    "Ide Konten":     ContentType.IDEAS,
    "Script Video":   ContentType.SCRIPT,
    "Caption":        ContentType.CAPTION,
    "Paket Lengkap":  ContentType.FULL_PACKAGE,
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EduGen — AI Content Generator")
        self.geometry("960x700")
        self.minsize(820, 600)
        self.configure(fg_color=BG)
        self._set_icon()
        self._build()

    # ── Icon ───────────────────────────────────────────────────────────────
    def _set_icon(self):
        ico = Path(__file__).parent / "icon.ico"
        if ico.exists():
            try:
                self.iconbitmap(str(ico))
            except Exception:
                pass

    # ── Layout ─────────────────────────────────────────────────────────────
    def _build(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._sidebar()
        self._main_panel()

    # ── Sidebar ────────────────────────────────────────────────────────────
    def _sidebar(self):
        sb = ctk.CTkFrame(self, width=260, fg_color=CARD, corner_radius=0)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_rowconfigure(10, weight=1)

        # Logo area
        logo_frame = ctk.CTkFrame(sb, fg_color=CARD2, corner_radius=0, height=90)
        logo_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        logo_frame.grid_propagate(False)

        ctk.CTkLabel(
            logo_frame, text="⚡ EduGen",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT,
        ).place(relx=0.5, rely=0.42, anchor="center")
        ctk.CTkLabel(
            logo_frame, text="AI Content Generator",
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
        ).place(relx=0.5, rely=0.75, anchor="center")

        pad = {"padx": 18, "pady": 6}

        # Tipe konten
        ctk.CTkLabel(sb, text="TIPE KONTEN", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=MUTED).grid(row=1, column=0, sticky="w", padx=18, pady=(20, 4))

        self.type_var = ctk.StringVar(value="Ide Konten")
        self.type_seg = ctk.CTkSegmentedButton(
            sb, values=list(TYPE_MAP.keys()),
            variable=self.type_var,
            command=self._on_type_change,
            fg_color=CARD2, selected_color=BRAND2, selected_hover_color=BRAND,
            unselected_color=CARD2, unselected_hover_color="#2a3828",
            text_color=TEXT, font=ctk.CTkFont(size=11),
            width=224,
        )
        self.type_seg.grid(row=2, column=0, **pad)

        # Topik
        ctk.CTkLabel(sb, text="TOPIK / TOKOH", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=MUTED).grid(row=3, column=0, sticky="w", padx=18, pady=(14, 4))
        self.topic_entry = ctk.CTkEntry(
            sb, placeholder_text='cth: "Ibnu Sina"',
            fg_color=CARD2, border_color="#3a4f38", text_color=TEXT,
            placeholder_text_color=MUTED, height=38, width=224,
            font=ctk.CTkFont(size=13),
        )
        self.topic_entry.grid(row=4, column=0, **pad)

        # Options frame (berubah sesuai tipe)
        self.opt_frame = ctk.CTkFrame(sb, fg_color="transparent")
        self.opt_frame.grid(row=5, column=0, sticky="ew", padx=18, pady=4)
        self._render_options()

        # Generate button
        self.gen_btn = ctk.CTkButton(
            sb, text="  Generate  ▶",
            command=self._generate,
            fg_color=BRAND2, hover_color=BRAND,
            text_color="#ffffff", font=ctk.CTkFont(size=14, weight="bold"),
            height=44, corner_radius=10, width=224,
        )
        self.gen_btn.grid(row=6, column=0, padx=18, pady=(18, 6))

        # Copy button
        self.copy_btn = ctk.CTkButton(
            sb, text="  Salin Hasil",
            command=self._copy,
            fg_color=CARD2, hover_color="#2a3828",
            text_color=MUTED, font=ctk.CTkFont(size=12),
            height=36, corner_radius=10, width=224, border_width=1,
            border_color="#3a4f38",
        )
        self.copy_btn.grid(row=7, column=0, padx=18, pady=4)

        # Status
        self.status_var = ctk.StringVar(value="Siap")
        ctk.CTkLabel(sb, textvariable=self.status_var,
                     font=ctk.CTkFont(size=10), text_color=MUTED,
                     wraplength=220).grid(row=10, column=0, sticky="sw", padx=18, pady=12)

    def _render_options(self):
        for w in self.opt_frame.winfo_children():
            w.destroy()

        t = self.type_var.get()

        if t == "Ide Konten":
            ctk.CTkLabel(self.opt_frame, text="JUMLAH IDE", font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=MUTED).pack(anchor="w", pady=(10, 3))
            self.count_var = ctk.IntVar(value=5)
            ctk.CTkSlider(self.opt_frame, from_=1, to=20, number_of_steps=19,
                          variable=self.count_var,
                          button_color=ACCENT, button_hover_color=BRAND,
                          progress_color=BRAND2, fg_color=CARD2,
                          width=224).pack(anchor="w")
            self.count_lbl = ctk.CTkLabel(self.opt_frame, text="5 ide",
                                          font=ctk.CTkFont(size=11), text_color=ACCENT)
            self.count_lbl.pack(anchor="w")
            self.count_var.trace_add("write", lambda *_: self.count_lbl.configure(
                text=f"{self.count_var.get()} ide"))

        elif t in ("Script Video", "Paket Lengkap"):
            ctk.CTkLabel(self.opt_frame, text="DURASI (MENIT)", font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=MUTED).pack(anchor="w", pady=(10, 3))
            self.dur_var = ctk.IntVar(value=10)
            ctk.CTkSlider(self.opt_frame, from_=3, to=20, number_of_steps=17,
                          variable=self.dur_var,
                          button_color=ACCENT, button_hover_color=BRAND,
                          progress_color=BRAND2, fg_color=CARD2,
                          width=224).pack(anchor="w")
            self.dur_lbl = ctk.CTkLabel(self.opt_frame, text="10 menit",
                                        font=ctk.CTkFont(size=11), text_color=ACCENT)
            self.dur_lbl.pack(anchor="w")
            self.dur_var.trace_add("write", lambda *_: self.dur_lbl.configure(
                text=f"{self.dur_var.get()} menit"))

        elif t == "Caption":
            ctk.CTkLabel(self.opt_frame, text="PLATFORM", font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=MUTED).pack(anchor="w", pady=(10, 3))
            self.platform_var = ctk.StringVar(value="Instagram")
            for p in PLATFORM_MAP:
                ctk.CTkRadioButton(
                    self.opt_frame, text=p, variable=self.platform_var, value=p,
                    fg_color=BRAND, hover_color=BRAND2, text_color=TEXT,
                    font=ctk.CTkFont(size=12),
                ).pack(anchor="w", pady=2)

    def _on_type_change(self, _=None):
        self._render_options()

    # ── Main panel ─────────────────────────────────────────────────────────
    def _main_panel(self):
        panel = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        panel.grid(row=0, column=1, sticky="nsew", padx=0)
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        # Header bar
        hdr = ctk.CTkFrame(panel, fg_color=CARD, height=55, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        self.hdr_label = ctk.CTkLabel(
            hdr, text="Hasil akan tampil di sini",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT,
        )
        self.hdr_label.place(relx=0.03, rely=0.5, anchor="w")

        self.token_label = ctk.CTkLabel(
            hdr, text="", font=ctk.CTkFont(size=10), text_color=MUTED,
        )
        self.token_label.place(relx=0.97, rely=0.5, anchor="e")

        # Output box
        self.output = ctk.CTkTextbox(
            panel, fg_color=CARD, text_color=TEXT,
            font=ctk.CTkFont(family="Consolas", size=13),
            scrollbar_button_color=CARD2,
            wrap="word", corner_radius=0,
            border_width=0,
        )
        self.output.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.output.insert("end", _WELCOME)
        self.output.configure(state="disabled")

    # ── Actions ────────────────────────────────────────────────────────────
    def _generate(self):
        topic = self.topic_entry.get().strip()
        tipe  = self.type_var.get()

        if not topic:
            self._set_output("Isi dulu topik / nama tokoh di kolom sebelah kiri.", "Topik kosong")
            return

        self.gen_btn.configure(state="disabled", text="  Generating...")
        self.status_var.set("Menghubungi Claude AI...")
        self._set_output("Sedang generate konten...\n\nMohon tunggu sebentar.", f"{tipe}: {topic}")
        threading.Thread(target=self._run_generate, args=(topic, tipe), daemon=True).start()

    def _run_generate(self, topic, tipe):
        try:
            result_text = ""
            tokens = 0
            saved_path = ""

            if tipe == "Ide Konten":
                count = getattr(self, "count_var", None)
                count = count.get() if count else 5
                req = ContentRequest(topic=topic, content_type=ContentType.IDEAS,
                                     theme=topic, idea_count=count)
                result = generate_ideas(req)
                result_text = result.content
                tokens = result.tokens_used
                saved_path = str(save_content(result))

            elif tipe == "Script Video":
                dur = getattr(self, "dur_var", None)
                dur = dur.get() if dur else 10
                req = ContentRequest(topic=topic, content_type=ContentType.SCRIPT,
                                     duration_minutes=dur)
                result = generate_script(req)
                result_text = result.content
                tokens = result.tokens_used
                saved_path = str(save_content(result))

            elif tipe == "Caption":
                plat_name = getattr(self, "platform_var", None)
                plat_name = plat_name.get() if plat_name else "Instagram"
                platform  = PLATFORM_MAP[plat_name]
                req = ContentRequest(topic=topic, content_type=ContentType.CAPTION,
                                     platform=platform)
                result = generate_caption(req)
                result_text = result.content
                tokens = result.tokens_used
                saved_path = str(save_content(result))

            elif tipe == "Paket Lengkap":
                dur = getattr(self, "dur_var", None)
                dur = dur.get() if dur else 10
                self.after(0, lambda: self.status_var.set("Generating paket lengkap (5 langkah)..."))
                package = generate_full_package(topic=topic, duration_minutes=dur)
                pkg_dir = save_package(package)
                result_text = _format_package(package)
                tokens = package.total_tokens
                saved_path = str(pkg_dir)

            self.after(0, lambda: self._on_done(result_text, tokens, saved_path, tipe, topic))

        except Exception as e:
            self.after(0, lambda: self._on_error(str(e)))

    def _on_done(self, text, tokens, path, tipe, topic):
        self._set_output(text, f"{tipe}: {topic}")
        self.token_label.configure(text=f"tokens: {tokens:,}  |  disimpan: {Path(path).name}")
        self.status_var.set(f"Selesai  —  {Path(path).name}")
        self.gen_btn.configure(state="normal", text="  Generate  ▶")

    def _on_error(self, msg):
        self._set_output(f"Error:\n\n{msg}", "Error")
        self.status_var.set("Error")
        self.gen_btn.configure(state="normal", text="  Generate  ▶")

    def _set_output(self, text, header=""):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.configure(state="disabled")
        if header:
            self.hdr_label.configure(text=header)

    def _copy(self):
        text = self.output.get("1.0", "end").strip()
        if text and text != _WELCOME.strip():
            self.clipboard_clear()
            self.clipboard_append(text)
            self.copy_btn.configure(text="  Tersalin!")
            self.after(1500, lambda: self.copy_btn.configure(text="  Salin Hasil"))


def _format_package(pkg) -> str:
    lines = [f"PAKET LENGKAP: {pkg.topic}\n{'='*60}\n"]
    if pkg.script:
        lines += ["\n[ SCRIPT VIDEO ]\n" + "-"*40 + "\n", pkg.script.content, "\n"]
    for k, cap in pkg.captions.items():
        lines += [f"\n[ CAPTION {k.upper()} ]\n" + "-"*40 + "\n", cap.content, "\n"]
    if pkg.thumbnail:
        lines += ["\n[ KONSEP THUMBNAIL ]\n" + "-"*40 + "\n", pkg.thumbnail.content]
    return "".join(lines)


_WELCOME = """
  Selamat datang di EduGen ⚡

  Auto-generate konten edukasi Indonesia berkualitas tinggi
  — tentang tokoh bersejarah, sains, produktivitas & kebijaksanaan.

  ──────────────────────────────────────────────

  Cara pakai:

  1. Pilih tipe konten di sidebar kiri
  2. Ketik topik / nama tokoh
  3. Atur opsi (durasi, jumlah, platform)
  4. Klik tombol  Generate ▶

  ──────────────────────────────────────────────

  Contoh topik yang bagus:

  • Ibnu Sina
  • Al-Khawarizmi
  • Nikola Tesla
  • Marie Curie
  • Ibn Khaldun
  • Epictetus
  • Leonardo da Vinci

"""


if __name__ == "__main__":
    app = App()
    app.mainloop()
