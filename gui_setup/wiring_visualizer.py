import tkinter as tk

# Theme Colors (Dark Mode Compatible)
COL_BG = "#2b2b2b"  # Background
COL_FG = "#eeeeee"  # Lines/Text
COL_POS = "#ff5555"  # Positive (Red)
COL_NEG = "#ffffff"  # Negative (White)
COL_JUMP = "#55aaff"  # Internal Jumpers (Blue)
COL_AMP = "#444444"  # Amp Body


class WiringVisualizer(tk.Canvas):
    def __init__(self, master, width=380, height=200, bg=COL_BG):
        super().__init__(master, width=width, height=height, bg=bg, highlightthickness=0)
        self.width = width
        self.height = height

        # State variables
        self.scale_factor = 1.0
        self.last_mouse_x = 0
        self.last_mouse_y = 0

        # Default draw parameters
        self.last_draw_params = (1, 1, "Single VC", "Series")

        # Bind events for interactivity
        self.bind("<ButtonPress-1>", self.start_pan)
        self.bind("<B1-Motion>", self.pan)
        self.bind("<MouseWheel>", self.zoom)  # Windows/MacOS
        self.bind("<Button-4>", self.zoom)  # Linux Scroll Up
        self.bind("<Button-5>", self.zoom)  # Linux Scroll Down

    def start_pan(self, event):
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def pan(self, event):
        # Calculate delta
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y

        # Move all objects with the tag "diagram"
        self.move("diagram", dx, dy)

        # Update last position
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def zoom(self, event):
        # Determine zoom direction and factor
        if event.num == 5 or event.delta < 0:
            factor = 0.9  # Zoom out
        else:
            factor = 1.1  # Zoom in

        # Limit zoom (0.1x to 10.0x)
        new_scale = self.scale_factor * factor
        if 0.1 < new_scale < 10.0:
            self.scale_factor = new_scale
            # Zoom centered on mouse pointer
            x = self.canvasx(event.x)
            y = self.canvasy(event.y)
            self.scale("diagram", x, y, factor, factor)

    def reset_view(self):
        """Resets zoom and pan by redrawing the diagram from scratch."""
        self.scale_factor = 1.0
        # Redraw using the last used parameters
        if hasattr(self, 'last_draw_params'):
            self.update_diagram(*self.last_draw_params)

    def draw_amp(self, x, y, w, h):
        """Draws the Amplifier block with terminals on the right."""
        # Amp Body
        self.create_rectangle(x, y, x + w, y + h, outline=COL_FG, width=2, fill=COL_AMP, tags="diagram")

        # Text
        self.create_text(x + w / 2, y + h / 2, text="AMP", fill=COL_FG, font=("Arial", 10, "bold"), angle=90,
                         tags="diagram")

        # Terminals
        term_y_pos = y + h / 3
        term_y_neg = y + 2 * h / 3

        # Pos Terminal (+)
        self.create_rectangle(x + w - 6, term_y_pos - 6, x + w, term_y_pos + 6, fill=COL_POS, outline="",
                              tags="diagram")
        self.create_text(x + w - 12, term_y_pos, text="+", fill=COL_BG, font=("Arial", 9, "bold"), tags="diagram")

        # Neg Terminal (-)
        self.create_rectangle(x + w - 6, term_y_neg - 6, x + w, term_y_neg + 6, fill=COL_NEG, outline="",
                              tags="diagram")
        self.create_text(x + w - 12, term_y_neg, text="-", fill=COL_BG, font=("Arial", 11, "bold"), tags="diagram")

        # Return terminal coordinates for wire connection
        return (x + w, term_y_pos), (x + w, term_y_neg)

    def draw_speaker(self, x, y, size=60, label="", vc_type="Single VC", vc_wiring="Series"):
        """Draws a speaker symbol. Visualizes Single vs Dual coils and internal wiring."""
        # Driver Frame
        self.create_rectangle(x, y, x + size, y + size, outline=COL_FG, width=2, fill="#333333", tags="diagram")

        # Y-Coordinates for Terminals (Top=Positive, Bottom=Negative)
        y_top = y + size / 3  # Positive rail height
        y_bot = y + 2 * size / 3  # Negative rail height

        # Text Padding (Gap between text center and wire start/end)
        txt_gap = 10

        # Draw Coils
        if vc_type == "Single VC":
            # Single large circle
            m = 4
            self.create_oval(x + m, y + m, x + size - m, y + size - m, outline=COL_FG, tags="diagram")

            # Center X of coil
            cx = x + size / 2

            # Wire: Input -> Text(+)
            self.create_line(x, y_top, cx - txt_gap, y_top, fill=COL_POS, width=1, tags="diagram")
            # Wire: Text(-) -> Output
            self.create_line(cx + txt_gap, y_bot, x + size, y_bot, fill=COL_NEG, width=1, tags="diagram")

            # Polarity Text
            self.create_text(cx, y_top, text="+", fill=COL_POS, font=("Arial", 16, "bold"), tags="diagram")
            self.create_text(cx, y_bot, text="-", fill=COL_NEG, font=("Arial", 16, "bold"), tags="diagram")

        elif vc_type == "Dual VC":
            # Two vertical oval coils side-by-side
            coil_w = (size - 12) / 2
            coil_h = size - 8
            c1_x = x + 4
            c2_x = x + 8 + coil_w
            cy = y + 4

            self.create_oval(c1_x, cy, c1_x + coil_w, cy + coil_h, outline=COL_FG, tags="diagram")  # Coil 1
            self.create_oval(c2_x, cy, c2_x + coil_w, cy + coil_h, outline=COL_FG, tags="diagram")  # Coil 2

            # Center X for each coil text
            c1_cx = c1_x + coil_w / 2
            c2_cx = c2_x + coil_w / 2

            # Polarity Text (Draw first)
            # Coil 1
            self.create_text(c1_cx, y_top, text="+", fill=COL_POS, font=("Arial", 16, "bold"), tags="diagram")  # C1+

            # Coil 2
            # C2+ is always Red (Positive)
            self.create_text(c2_cx, y_top, text="+", fill=COL_POS, font=("Arial", 16, "bold"), tags="diagram")  # C2+
            # C2- is always White (Negative)
            self.create_text(c2_cx, y_bot, text="-", fill=COL_NEG, font=("Arial", 16, "bold"), tags="diagram")  # C2-

            # Internal Wiring Logic (The Blue Jumper)
            if vc_wiring == "Series":
                # C1- is always White (Negative), even if connected to a jumper
                self.create_text(c1_cx, y_bot, text="-", fill=COL_NEG, font=("Arial", 16, "bold"),
                                 tags="diagram")  # C1-

                # 1. Input (Red) -> C1 Positive (Top Left)
                self.create_line(x, y_top, c1_cx - txt_gap, y_top, fill=COL_POS, width=2, tags="diagram")

                # 2. Jumper (Blue): C1 Negative (Top Right) -> C2 Positive (Top Left)
                # Diagonal cross from bottom-left coil to top-right coil
                self.create_line(c1_cx + txt_gap, y_bot, c2_cx - txt_gap, y_top, fill=COL_JUMP, width=2, tags="diagram")

                # 3. Output (White): C2 Negative (Top Right) -> Exit (Bottom Right)
                # Diagonal drop from text to negative terminal
                self.create_line(c2_cx + txt_gap, y_bot, x + size, y_bot, fill=COL_NEG, width=2, tags="diagram")

            elif vc_wiring == "Parallel":
                # C1- is Neg/White
                self.create_text(c1_cx, y_bot, text="-", fill=COL_NEG, font=("Arial", 16, "bold"), tags="diagram")

                # 1. Input (Red) -> C1+
                self.create_line(x, y_top, c1_cx - txt_gap, y_top, fill=COL_POS, width=2, tags="diagram")

                # 2. Pos Jumper (Blue): C1+ -> C2+
                self.create_line(c1_cx + txt_gap, y_top, c2_cx - txt_gap, y_top, fill=COL_JUMP, width=2, tags="diagram")

                # 3. Output (White): Exit <- C2-
                self.create_line(x + size, y_bot, c2_cx + txt_gap, y_bot, fill=COL_NEG, width=2, tags="diagram")

                # 4. Neg Jumper (Blue): C2- -> C1-
                self.create_line(c2_cx - txt_gap, y_bot, c1_cx + txt_gap, y_bot, fill=COL_JUMP, width=2, tags="diagram")

        # Draw External Terminal Stubs (Visual anchor points)
        self.create_line(x, y_top, x - 4, y_top, fill=COL_POS, width=2, tags="diagram")
        self.create_line(x + size, y_bot, x + size + 4, y_bot, fill=COL_NEG, width=2, tags="diagram")

        # Label (e.g. "1-2")
        if label:
            self.create_text(x + size / 2, y + size + 8, text=label, fill="#888888", font=("Arial", 8), tags="diagram")

    def update_diagram(self, s_groups, p_groups, vc_type="Single VC", vc_wiring="Series"):
        """Draws the complete schematic."""
        self.last_draw_params = (s_groups, p_groups, vc_type, vc_wiring)  # Save params for reset
        self.delete("all")
        self.scale_factor = 1.0  # Reset zoom

        # Dimensions - INCREASED SIZE FOR CLARITY
        amp_w = 50
        amp_h = 120
        spk_size = 60  # Increased from 40 to fit 16pt text
        gap_x = 40  # Space between series speakers
        gap_y = 30  # Space between parallel rows

        # Render Limits
        render_s = s_groups
        render_p = p_groups

        # 1. Draw Amplifier (Left Centered)
        amp_x = 10
        amp_y = (self.height - amp_h) / 2
        (amp_pos_x, amp_pos_y), (amp_neg_x, amp_neg_y) = self.draw_amp(amp_x, amp_y, amp_w, amp_h)

        # 2. Calculate Array Block Position
        block_w = (render_s * spk_size) + ((render_s - 1) * gap_x)
        block_h = (render_p * spk_size) + ((render_p - 1) * gap_y)

        # Start drawing speakers to the right of Amp
        start_x = amp_pos_x + 40
        start_y = (self.height - block_h) / 2

        # 3. Draw Main Power Rails
        # Pos Rail (Red): From Amp+ straight across to the last column
        rail_top_y = amp_pos_y
        self.create_line(amp_pos_x, rail_top_y, start_x - 15, rail_top_y, fill=COL_POS, width=2, tags="diagram")

        # Neg Rail (White): We'll collect all returns on the far right
        rail_return_x = start_x + block_w + 20

        # 4. Draw Rows
        for p in range(render_p):
            row_y = start_y + (p * (spk_size + gap_y))
            spk_pos_y = row_y + spk_size / 3
            spk_neg_y = row_y + 2 * spk_size / 3

            # Connect Row Start to Pos Rail
            # Vertical drop line from main rail to this row
            self.create_line(start_x - 15, rail_top_y, start_x - 15, spk_pos_y, fill=COL_POS, width=2, tags="diagram")
            self.create_line(start_x - 15, spk_pos_y, start_x, spk_pos_y, fill=COL_POS, width=2, tags="diagram")

            # Connect Row End to Return Rail
            self.create_line(start_x + block_w, spk_neg_y, rail_return_x, spk_neg_y, fill=COL_NEG, width=2,
                             tags="diagram")

            # Draw Speakers in Series
            for s in range(render_s):
                curr_x = start_x + (s * (spk_size + gap_x))
                label = f"{p + 1}-{s + 1}"

                self.draw_speaker(curr_x, row_y, spk_size, label, vc_type, vc_wiring)

                # Interconnect (Blue): Connect Neg of current to Pos of next
                if s < render_s - 1:
                    self.create_line(curr_x + spk_size + 4, spk_neg_y,
                                     curr_x + spk_size + gap_x - 4, spk_pos_y,
                                     fill=COL_JUMP, width=2, tags="diagram")  # Diagonal connection

        # Connect Return Rail back to Amp
        # Route below everything
        return_path_y = start_y + block_h + 20
        safe_bottom_y = max(return_path_y, amp_y + amp_h + 20)

        self.create_line(rail_return_x, start_y + 2 * spk_size / 3, rail_return_x, safe_bottom_y, fill=COL_NEG, width=2,
                         tags="diagram")  # Down
        self.create_line(rail_return_x, safe_bottom_y, amp_neg_x + 15, safe_bottom_y, fill=COL_NEG, width=2,
                         tags="diagram")  # Left
        self.create_line(amp_neg_x + 15, safe_bottom_y, amp_neg_x + 15, amp_neg_y, fill=COL_NEG, width=2,
                         tags="diagram")  # Up
        self.create_line(amp_neg_x + 15, amp_neg_y, amp_neg_x, amp_neg_y, fill=COL_NEG, width=2,
                         tags="diagram")  # Connect

        # Truncation Text
        if s_groups > render_s or p_groups > render_p:
            txt = f"Diagram clipped: Showing {render_s}x{render_p} of actual {s_groups}x{p_groups}"
            self.create_text(self.width / 2, self.height - 10, text=txt, fill="#666666", font=("Arial", 8),
                             tags="diagram")