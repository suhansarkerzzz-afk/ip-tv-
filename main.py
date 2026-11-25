
import csv, json, re, threading, time, queue, webbrowser
from pathlib import Path
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import requests
except ImportError:
    requests = None

APP_NAME = "IPTV Channel Extractor Pro"
DEFAULT_URL = "https://iptv-org.github.io/iptv/index.m3u"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1280x780")
        self.root.minsize(1050, 650)
        self.dark = True
        self.channels = []
        self.filtered = []
        self.stop_check = False
        self.msgq = queue.Queue()
        self.colors = {
            "bg":"#0b1020","panel":"#111827","panel2":"#182235","fg":"#eef2ff",
            "muted":"#9ca3af","accent":"#7c3aed","accent2":"#2563eb",
            "green":"#22c55e","red":"#ef4444","yellow":"#f59e0b","line":"#263247"
        }
        self.build_style()
        self.build_ui()
        self.root.after(100, self.process_queue)

    def build_style(self):
        c=self.colors
        s=ttk.Style()
        s.theme_use("clam")
        s.configure("TFrame", background=c["bg"])
        s.configure("Panel.TFrame", background=c["panel"])
        s.configure("TLabel", background=c["bg"], foreground=c["fg"], font=("Segoe UI",10))
        s.configure("Title.TLabel", background=c["bg"], foreground=c["fg"], font=("Segoe UI",22,"bold"))
        s.configure("Sub.TLabel", background=c["bg"], foreground=c["muted"], font=("Segoe UI",10))
        s.configure("TButton", background=c["panel2"], foreground=c["fg"], borderwidth=0, padding=(14,8), font=("Segoe UI",10,"bold"))
        s.map("TButton", background=[("active",c["accent"])])
        s.configure("Accent.TButton", background=c["accent"], foreground="white")
        s.map("Accent.TButton", background=[("active",c["accent2"])])
        s.configure("TEntry", fieldbackground=c["panel2"], foreground=c["fg"], insertcolor=c["fg"], borderwidth=0, padding=8)
        s.configure("TCombobox", fieldbackground=c["panel2"], foreground=c["fg"])
        s.configure("Treeview", background=c["panel"], fieldbackground=c["panel"], foreground=c["fg"], rowheight=32, borderwidth=0, font=("Segoe UI",9))
        s.configure("Treeview.Heading", background=c["panel2"], foreground=c["fg"], relief="flat", font=("Segoe UI",9,"bold"))
        s.map("Treeview", background=[("selected",c["accent"])], foreground=[("selected","white")])
        s.configure("Horizontal.TProgressbar", troughcolor=c["panel2"], background=c["accent"], borderwidth=0)

    def build_ui(self):
        c=self.colors
        outer=ttk.Frame(self.root); outer.pack(fill="both",expand=True,padx=18,pady=14)
        head=ttk.Frame(outer); head.pack(fill="x")
        ttk.Label(head,text="📺 IPTV Channel Extractor Pro",style="Title.TLabel").pack(side="left")
        ttk.Button(head,text="☀ / 🌙 Theme",command=self.toggle_theme).pack(side="right",padx=4)
        ttk.Button(head,text="ℹ Help",command=self.help).pack(side="right",padx=4)
        ttk.Label(outer,text="Download, parse, search, validate and export IPTV playlist entries.",style="Sub.TLabel").pack(anchor="w",pady=(2,12))
        urlrow=ttk.Frame(outer); urlrow.pack(fill="x")
        self.url=tk.StringVar(value=DEFAULT_URL)
        ttk.Entry(urlrow,textvariable=self.url).pack(side="left",fill="x",expand=True)
        ttk.Button(urlrow,text="LOAD PLAYLIST",style="Accent.TButton",command=self.load).pack(side="left",padx=(8,0))
        ttk.Button(urlrow,text="CLEAR",command=self.clear_all).pack(side="left",padx=(6,0))
        toolbar=ttk.Frame(outer); toolbar.pack(fill="x",pady=10)
        self.search=tk.StringVar()
        e=ttk.Entry(toolbar,textvariable=self.search)
        e.pack(side="left",fill="x",expand=True); self.search.trace_add("write",lambda *_:self.apply_filter())
        ttk.Button(toolbar,text="🗑 Clear Search",command=lambda:self.search.set("")).pack(side="left",padx=6)
        ttk.Button(toolbar,text="COPY SELECTED URL",command=self.copy_selected).pack(side="left",padx=3)
        ttk.Button(toolbar,text="OPEN STREAM",command=self.open_selected).pack(side="left",padx=3)
        stats=ttk.Frame(outer); stats.pack(fill="x",pady=(0,10))
        self.stat_vars={k:tk.StringVar(value=f"{k}: 0") for k in ["TOTAL","WORKING","DEAD","UNKNOWN"]}
        for k in self.stat_vars:
            ttk.Label(stats,textvariable=self.stat_vars[k],style="Sub.TLabel").pack(side="left",padx=(0,20))
        tableframe=ttk.Frame(outer); tableframe.pack(fill="both",expand=True)
        cols=("name","group","country","language","status","url")
        self.tree=ttk.Treeview(tableframe,columns=cols,show="headings",selectmode="extended")
        widths={"name":250,"group":150,"country":85,"language":110,"status":100,"url":520}
        heads={"name":"CHANNEL","group":"GROUP","country":"COUNTRY","language":"LANGUAGE","status":"STATUS","url":"STREAM URL"}
        for col in cols:
            self.tree.heading(col,text=heads[col])
            self.tree.column(col,width=widths[col],anchor="w")
        vs=ttk.Scrollbar(tableframe,orient="vertical",command=self.tree.yview)
        hs=ttk.Scrollbar(tableframe,orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=vs.set,xscrollcommand=hs.set)
        self.tree.grid(row=0,column=0,sticky="nsew"); vs.grid(row=0,column=1,sticky="ns"); hs.grid(row=1,column=0,sticky="ew")
        tableframe.rowconfigure(0,weight=1); tableframe.columnconfigure(0,weight=1)
        bottom=ttk.Frame(outer); bottom.pack(fill="x",pady=(10,0))
        self.progress=ttk.Progressbar(bottom,mode="determinate"); self.progress.pack(side="left",fill="x",expand=True)
        self.status=tk.StringVar(value="Ready")
        ttk.Label(bottom,textvariable=self.status,style="Sub.TLabel").pack(side="left",padx=10)
        ttk.Button(bottom,text="CHECK ALL",command=self.check_all).pack(side="right",padx=3)
        ttk.Button(bottom,text="STOP",command=self.stop_checks).pack(side="right",padx=3)
        ttk.Button(bottom,text="EXPORT CSV",command=self.export_csv).pack(side="right",padx=3)
        ttk.Button(bottom,text="EXPORT JSON",command=self.export_json).pack(side="right",padx=3)

    def toggle_theme(self):
        self.dark=not self.dark
        messagebox.showinfo("Theme","Theme preference toggled. Restarting the window styling is not required for data.")

    def help(self):
        messagebox.showinfo(APP_NAME,
            "LOAD downloads an M3U/M3U8 playlist and extracts channel metadata + stream URLs.\n\n"
            "CHECK ALL performs lightweight HTTP checks. Some legitimate streams may reject HEAD requests or require special headers, so status is not a guarantee of playback.\n\n"
            "COPY SELECTED URL copies the selected stream URL to the clipboard.\n"
            "Exports include the current extracted/filtered dataset.")

    def clear_all(self):
        self.channels=[]; self.filtered=[]; self.search.set("")
        for x in self.tree.get_children(): self.tree.delete(x)
        for k in self.stat_vars: self.stat_vars[k].set(f"{k}: 0")
        self.progress["value"]=0; self.status.set("Cleared")

    def parse_attr(self, line, key):
        m=re.search(rf'{re.escape(key)}="([^"]*)"',line,re.I)
        return m.group(1).strip() if m else ""

    def parse_m3u(self,text):
        lines=text.splitlines()
        out=[]; pending=None
        for raw in lines:
            line=raw.strip()
            if not line: continue
            if line.upper().startswith("#EXTINF"):
                name=line.split(",",1)[1].strip() if "," in line else "Unknown"
                pending={"name":name,"group":self.parse_attr(line,"group-title"),
                    "country":self.parse_attr(line,"tvg-country"),"language":self.parse_attr(line,"tvg-language"),
                    "logo":self.parse_attr(line,"tvg-logo"),"id":self.parse_attr(line,"tvg-id"),
                    "status":"Unknown","url":""}
            elif pending and not line.startswith("#"):
                if line.startswith(("http://","https://","rtmp://","rtsp://")):
                    pending["url"]=line
                    out.append(pending); pending=None
        seen=set(); clean=[]
        for x in out:
            key=(x["name"].casefold(),x["url"].strip())
            if key in seen: continue
            seen.add(key); clean.append(x)
        return clean

    def load(self):
        if requests is None:
            messagebox.showerror("Missing dependency","Run install.bat first."); return
        u=self.url.get().strip()
        if not u: return
        self.status.set("Downloading playlist..."); self.progress["value"]=0
        threading.Thread(target=self._load_worker,args=(u,),daemon=True).start()

    def _load_worker(self,u):
        try:
            r=requests.get(u,timeout=90,headers={"User-Agent":"IPTV-Channel-Extractor-Pro/1.0"})
            r.raise_for_status(); chans=self.parse_m3u(r.text)
            self.msgq.put(("loaded",chans,len(r.content)))
        except Exception as e: self.msgq.put(("error",f"Download/parse failed: {e}"))

    def apply_filter(self):
        q=self.search.get().casefold().strip()
        if not q: self.filtered=list(self.channels)
        else: self.filtered=[x for x in self.channels if q in " ".join([x["name"],x["group"],x["country"],x["language"],x["url"]]).casefold()]
        self.refresh_table()

    def refresh_table(self):
        for x in self.tree.get_children(): self.tree.delete(x)
        for x in self.filtered:
            self.tree.insert("", "end", values=(x["name"],x["group"],x["country"],x["language"],x["status"],x["url"]))
        self.update_stats()

    def update_stats(self):
        self.stat_vars["TOTAL"].set(f"TOTAL: {len(self.channels)}")
        self.stat_vars["WORKING"].set(f"WORKING: {sum(x['status']=='Working' for x in self.channels)}")
        self.stat_vars["DEAD"].set(f"DEAD: {sum(x['status']=='Dead' for x in self.channels)}")
        self.stat_vars["UNKNOWN"].set(f"UNKNOWN: {sum(x['status']=='Unknown' for x in self.channels)}")

    def selected_channel(self):
        sel=self.tree.selection()
        if not sel: return None
        vals=self.tree.item(sel[0],"values"); url=vals[5]
        for x in self.channels:
            if x["url"]==url and x["name"]==vals[0]: return x
        return None

    def copy_selected(self):
        x=self.selected_channel()
        if not x: messagebox.showwarning("Copy","Select a channel first."); return
        self.root.clipboard_clear(); self.root.clipboard_append(x["url"]); self.root.update()
        self.status.set("Stream URL copied")

    def open_selected(self):
        x=self.selected_channel()
        if x: webbrowser.open(x["url"])

    def check_all(self):
        if not self.channels: return
        self.stop_check=False
        threading.Thread(target=self._check_worker,daemon=True).start()

    def stop_checks(self): self.stop_check=True

    def _check_worker(self):
        total=len(self.channels)
        for i,x in enumerate(self.channels):
            if self.stop_check: break
            try:
                rr=requests.get(x["url"],headers={"User-Agent":"Mozilla/5.0","Range":"bytes=0-1023"},timeout=8,stream=True,allow_redirects=True)
                x["status"]="Working" if rr.status_code in (200,206,301,302,307,308) else "Dead"
                rr.close()
            except Exception: x["status"]="Dead"
            self.msgq.put(("progress",i+1,total))
        self.msgq.put(("checked",))

    def export_json(self):
        if not self.channels: return
        p=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON","*.json")],initialfile="channels.json")
        if p:
            Path(p).write_text(json.dumps(self.channels,ensure_ascii=False,indent=2),encoding="utf-8")
            self.status.set("JSON exported")

    def export_csv(self):
        if not self.channels: return
        p=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")],initialfile="channels.csv")
        if p:
            with open(p,"w",newline="",encoding="utf-8-sig") as f:
                w=csv.DictWriter(f,fieldnames=["name","group","country","language","logo","id","status","url"])
                w.writeheader(); w.writerows(self.channels)
            self.status.set("CSV exported")

    def process_queue(self):
        try:
            while True:
                m=self.msgq.get_nowait()
                if m[0]=="loaded":
                    self.channels=m[1]; self.apply_filter()
                    self.status.set(f"Loaded {len(self.channels):,} unique channels")
                elif m[0]=="error":
                    messagebox.showerror("Error",m[1]); self.status.set("Error")
                elif m[0]=="progress":
                    i,total=m[1],m[2]; self.progress["maximum"]=total; self.progress["value"]=i
                    if i%25==0 or i==total: self.status.set(f"Checking {i:,}/{total:,}")
                    self.refresh_table()
                elif m[0]=="checked":
                    self.refresh_table(); self.status.set("Check completed")
        except queue.Empty: pass
        self.root.after(100,self.process_queue)

if __name__=="__main__":
    root=tk.Tk()
    App(root)
    root.mainloop()
