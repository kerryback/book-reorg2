# Create Slides Skill

This skill is for building PowerPoint presentations (PPTX) from chapter QMD files with **fully automated high-quality LaTeX equation rendering**.

## Overview

This skill converts chapter QMD files (e.g., `Chapter_Intro_Options.qmd`) into professional PowerPoint presentations (PPTX) with zero manual intervention. The process extracts content, figures, and embedded resources, and **automatically renders all LaTeX equations to high-quality PNG images** using the native LaTeX engine (via tex2img), then inserts them directly into the PowerPoint slides.

## Workflow Steps

### Step 1: Analyze Chapter Structure
- Read the source `Chapter_*.qmd` file
- Identify major sections (headers starting with `##`)
- Catalog all figures and their labels (e.g., `#fig-long-call`)
- Identify all iframe embeds and their source URLs
- Note all LaTeX math expressions (inline `$...$` and display `$$...$$`)
- Extract callout boxes and special formatting

### Step 2: Create Slides QMD File
Generate a new `Slides_*.qmd` file with the following structure:

**YAML Header:**
```yaml
---
title: "Chapter Title"
format:
  pptx:
    reference-doc: custom-reference.pptx  # Optional: custom theme
---
```

**Content Organization:**
- Each major section (`##`) becomes a slide with a header
- Subsections (`###`) become new slides or bullet points depending on content depth
- Keep slides focused: 3-5 bullet points per slide maximum
- Math-heavy content: one key equation per slide with explanation

**Figure Handling:**
- Include figure code blocks in slides QMD
- Ensure figures are regenerated when rendering
- Add figure captions as slide notes or subtitle text
- For Python plots: ensure all required imports are included

**Iframe/External Resource Handling:**
- Extract iframe URLs from chapter
- Create slides with:
  - Link to the interactive resource
  - Screenshot or description of what the resource shows
  - Note: "Interactive version available at [URL]"

**LaTeX Handling:**
- Extract all `$...$` and `$$...$$` LaTeX code
- Render each equation to high-quality PNG using tex2img
- Replace LaTeX code with image placeholders in the slides
- Store rendered equation images with proper naming (equation_001.png, etc.)

### Step 3: Render LaTeX Equations to Images
Using **tex2img** (which uses native LaTeX → PDF → PNG pipeline):
```python
from tex2img import Latex2PNG

# For display equations
converter = Latex2PNG(r'\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2')
converter.save('equation_001.png', dpi=300)

# For inline equations
converter = Latex2PNG(r'C \geq \max(S - K, 0)', mode='inline')
converter.save('equation_002.png', dpi=300)
```

**Rendering Quality:**
- DPI: 300 (publication quality)
- Font: Computer Modern (native LaTeX font, same as Beamer)
- Transparent background for seamless integration
- Proper bounding boxes (tight crop)

### Step 4: Build PowerPoint with python-pptx
Using python-pptx to construct the final presentation:
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and content
slide.shapes.title.text = "Put-Call Parity"

# Add equation image
left = Inches(2)
top = Inches(3)
pic = slide.shapes.add_picture('equation_005.png', left, top, height=Inches(1))

prs.save('Slides_Intro_Options.pptx')
```

### Step 5: Custom Python Script
Build a custom script (`chapter_to_slides.py`) that:
1. Parses Chapter QMD file (sections, figures, math, iframes)
2. Extracts all LaTeX equations and renders them to PNG using tex2img
3. Generates slide structure with content organized by sections
4. Uses python-pptx to build PPTX directly (bypassing Quarto's poor math rendering)
5. Inserts equation images at appropriate positions
6. Adds Python-generated figures to slides
7. Creates link slides for iframe resources

## Design Considerations

### Slide Content Principles
- **One Idea Per Slide**: Each slide should convey a single concept
- **Visual Hierarchy**: Use headers, bullet points, and spacing
- **Math Presentation**: Display equations prominently, one per slide when complex
- **Code Examples**: Include only essential code, with simplified syntax
- **Figures**: Full-size plots with clear labels and legends

### PowerPoint Theme for Finance/Math
**Recommended Theme Settings:**
- **Background**: White or light gray gradient (subtle)
- **Header Color**: Navy blue (#003366) or dark teal (#006666)
- **Accent Colors**:
  - Orange (#FF6B35) for emphasis
  - Gold (#FFB700) for highlights
- **Fonts**:
  - Headers: Sans-serif (Arial, Calibri, or Helvetica)
  - Body: Sans-serif for readability
  - Math: Rendered by tex2img in Computer Modern (native LaTeX font)
- **Plot Colors**: Use colorblind-friendly palettes (viridis, colorbrewer)

### Automated LaTeX Rendering Strategy
**Fully Automated Pipeline:**
1. Script extracts all LaTeX equations from chapter QMD
2. tex2img renders each equation to PNG (300 DPI, transparent background)
3. python-pptx builds PowerPoint slides with equation images positioned automatically
4. **No manual steps required** - equations are publication-quality from the start

**Advantages over Manual IguanaTex:**
- **Zero manual intervention**: Batch process all chapters
- **Consistent quality**: Same rendering for all equations
- **Version control friendly**: PNG files can be committed to repo
- **Reproducible**: Re-run script to update all slides
- **Native LaTeX quality**: Same fonts as Beamer PDFs

## File Structure

For each chapter conversion, create:
```
Chapter_Topic.qmd              # Original chapter (input)
Slides_Topic.pptx              # Generated PowerPoint presentation
Slides_Topic_equations/        # Rendered equation images (PNG)
  equation_001.png
  equation_002.png
  ...
Slides_Topic_figures/          # Python-generated figures from chapter
  fig_long_call.png
  fig_put_call_parity.png
  ...
Slides_Topic_links.txt         # List of external resources (iframes)
Slides_Topic_structure.json    # Slide structure metadata (for debugging)
```

**Note:** No intermediate QMD file needed - we build PPTX directly from Chapter QMD using python-pptx.

## Implementation Scripts

### Script 1: `chapter_to_slides.py`
Main conversion script that:
- **Parses Chapter QMD**: Uses regex to identify sections, figures, LaTeX equations, iframes
- **Extracts LaTeX equations**: Finds all `$...$` and `$$...$$` blocks
- **Renders equations to PNG**: Uses tex2img with 300 DPI, transparent background
- **Extracts Python figures**: Executes figure code blocks and saves as PNG
- **Builds PowerPoint**: Uses python-pptx to create presentation structure
- **Inserts content**: Adds titles, bullets, equation images, figure images
- **Handles iframes**: Creates link slides with URLs to interactive resources

**Key Functions:**
```python
def parse_chapter(qmd_file):
    """Parse chapter QMD and extract structure."""
    return sections, equations, figures, iframes

def render_equations(equations, output_dir):
    """Render all LaTeX equations to PNG using tex2img."""
    for i, eq in enumerate(equations):
        converter = Latex2PNG(eq['latex'])
        converter.save(f'{output_dir}/equation_{i:03d}.png', dpi=300)

def build_presentation(structure, equation_images, figure_images):
    """Build PowerPoint using python-pptx."""
    prs = Presentation()
    # ... add slides with content ...
    return prs
```

### Script 2: `batch_convert.py`
Batch processing for multiple chapters:
- Takes list of chapter files or pattern (e.g., `Chapter_*.qmd`)
- Runs conversion for each chapter
- Generates summary report with statistics
- Creates index of all generated presentations

### Script 3: `preview_equations.py` (Optional)
Quick equation preview tool:
- Extract all equations from a chapter
- Render them in a grid layout for review
- Useful for checking equation quality before full conversion

## Usage Examples

### Single Chapter Conversion
```bash
python chapter_to_slides.py Chapter_Intro_Options.qmd
# Creates: Slides_Intro_Options.pptx (ready to present!)
# Also creates: Slides_Intro_Options_equations/ (PNG images)
#              Slides_Intro_Options_figures/ (Python plots)
```

### Batch Conversion
```bash
python batch_convert.py Chapter_*.qmd
# Processes all chapters, generates summary report
```

### Custom Theme
```bash
python chapter_to_slides.py Chapter_Intro_Options.qmd --theme finance-theme.pptx
# Uses custom PowerPoint template for consistent branding
```

### Preview Equations Only
```bash
python preview_equations.py Chapter_BlackScholes.qmd
# Renders all equations to a single PDF for quality check
```

## LaTeX Equation Handling Details

### Automated Rendering Pipeline

**Step 1: Extraction**
Script uses regex to find all LaTeX equations:
```python
import re

# Display equations
display_pattern = r'\$\$(.*?)\$\$'
display_equations = re.findall(display_pattern, content, re.DOTALL)

# Inline equations
inline_pattern = r'\$(.*?)\$'
inline_equations = re.findall(inline_pattern, content)
```

**Step 2: Rendering with tex2img**
```python
from tex2img import Latex2PNG

# Include custom LaTeX preamble from macros.qmd
preamble = r'''
\usepackage{amsmath}
\usepackage{amssymb}
\newcommand{\d}{\,\mathrm{d}}
\newcommand{\e}{\mathrm{e}}
\newcommand{\E}{\mathbb{E}}
'''

# Render display equation
latex_code = r'\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2'
converter = Latex2PNG(latex_code, preamble=preamble)
converter.save('equation_001.png', dpi=300, transparent=True)
```

**Step 3: Insertion into PowerPoint**
```python
from pptx.util import Inches

# Add equation image to slide
left = Inches(2)
top = Inches(3)
height = Inches(0.8)  # Auto-scale width to maintain aspect ratio
slide.shapes.add_picture('equation_001.png', left, top, height=height)
```

### Quality Settings
- **DPI**: 300 (publication quality, crisp on projection screens)
- **Font**: Computer Modern (native LaTeX, matches Beamer PDFs)
- **Background**: Transparent (blends with slide background)
- **Format**: PNG with alpha channel
- **Bounding Box**: Tight crop (no extra whitespace)

## Common Patterns

### Section to Slide Mapping
```
## Major Section          → Title slide
### Subsection           → Content slide with header
#### Sub-subsection      → Bullet point on parent slide

Callout boxes           → Highlighted box on slide
Code blocks             → Code slide with syntax highlighting
Figures                 → Full slide with figure + caption
Tables                  → Table slide with header
```

### Figure Code Handling
**In Chapter:**
```python
::: {#fig-long-call}
```{python}
#| label: fig-long-call
#| fig-cap: Caption text
import plotly.graph_objects as go
# ... plot code ...
fig.show()
```
:::
```

**Script Execution:**
```python
# Extract and execute figure code
fig_code = extract_figure_code(chapter, 'fig-long-call')
exec(fig_code)  # Generates the plot

# Modify for slide dimensions and save
fig.update_layout(width=800, height=500)
fig.write_image('Slides_Topic_figures/fig_long_call.png', scale=2)
```

**In Generated Slides:**
```python
# Script creates PowerPoint slide
slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout
slide.shapes.title.text = "Long Call Option"

# Add figure image
pic = slide.shapes.add_picture(
    'Slides_Topic_figures/fig_long_call.png',
    left=Inches(1),
    top=Inches(1.5),
    width=Inches(8)
)

# Add bullet points as text box
textbox = slide.shapes.add_textbox(...)
textbox.text = "• Maximum profit: unlimited\n• Maximum loss: premium paid"
```

### Iframe Handling
**In Chapter:**
```html
::: {#fig-options-market-data}
<iframe height="750" width="720" src="https://options-market-data.koyeb.app/"></iframe>
Options Market Data
:::
```

**Script Extraction:**
```python
# Extract iframe URL
iframe_pattern = r'<iframe[^>]*src="([^"]*)"'
url = re.search(iframe_pattern, content).group(1)
```

**In Generated Slides:**
```python
# Create link slide
slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and content
slide.shapes.title.text = "Options Market Data"

# Add hyperlink as text
textbox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(1))
text_frame = textbox.text_frame
p = text_frame.paragraphs[0]
run = p.add_run()
run.text = "Interactive tool: options-market-data.koyeb.app"
run.hyperlink.address = "https://options-market-data.koyeb.app/"

# Add description bullets
text_frame.text += "\n\nKey features:\n• Real-time bid/ask prices\n• Volume and open interest"
```

## Edge Cases and Special Handling

### Multi-Figure Layouts
- Chapter may have side-by-side figures
- Slides: separate these into individual slides or simplify layout

### Long Code Blocks
- Chapter may include complete implementations
- Slides: show only key lines, reference full code elsewhere

### Mathematical Derivations
- Chapter may show multi-step proofs
- Slides: show starting point, key steps, and result; details in notes

### Tables
- Large tables: summarize key rows/columns only
- Reference full table in appendix or supplementary materials

## Quality Checklist

Before finalizing slides:
- [ ] All major sections from chapter are represented
- [ ] No slide has more than 5-7 bullet points
- [ ] All figures render correctly and are readable
- [ ] LaTeX equations are preserved in source
- [ ] Equations file matches slides
- [ ] Links to external resources are included
- [ ] Slide titles are clear and descriptive
- [ ] Color scheme is consistent and professional
- [ ] Text is large enough for presentation (min 18pt)

## Future Enhancements

### Potential Improvements
1. **Automatic IguanaTex Integration**: PowerPoint VBA macro for batch equation rendering
2. **AI-Powered Summarization**: Use LLM to automatically generate slide bullet points from chapter prose
3. **Speaker Notes**: Extract relevant chapter text into PowerPoint speaker notes
4. **Slide Transitions**: Add appropriate animations for builds and reveals
5. **Theme Gallery**: Create multiple pre-designed themes for different presentation contexts
6. **Interactive Plots**: Embed interactive Plotly figures that work in PowerPoint
7. **Quiz Slides**: Generate assessment questions from chapter content
8. **Translation Support**: Multi-language slide generation

## Dependencies

### Required Software
- **Python 3.8+**
- **LaTeX distribution** (TeX Live, MiKTeX, or MacTeX) - already installed for Quarto
- **PowerPoint** (for viewing/editing final presentations)

### Python Packages
```bash
pip install tex2img python-pptx pyyaml plotly kaleido numpy
```

**Package purposes:**
- `tex2img`: LaTeX → PNG rendering (native LaTeX quality)
- `python-pptx`: PowerPoint file creation and manipulation
- `pyyaml`: YAML header parsing from QMD files
- `plotly`: Figure regeneration from chapter code
- `kaleido`: Plotly static image export
- `numpy`: Required for figure code execution

### LaTeX Configuration
The script will use your existing LaTeX installation. Ensure these are accessible:
- `pdflatex` (or `xelatex`)
- `dvipng` or `pdftoppm` (for PNG conversion)
- Standard packages: `amsmath`, `amssymb`, `amsfonts`

## Troubleshooting

### tex2img Rendering Fails
**Symptom:** Error when rendering equations
**Solutions:**
- Verify LaTeX is installed and in PATH: `pdflatex --version`
- Check custom macros from macros.qmd are included in preamble
- Test individual equation: `python -c "from tex2img import Latex2PNG; Latex2PNG('x^2').save('test.png')"`
- Ensure dvipng is installed: `dvipng --version`

### Equations Have Wrong Fonts
**Symptom:** Equations don't match expected Computer Modern font
**Solutions:**
- tex2img uses system LaTeX, which should default to Computer Modern
- Verify LaTeX packages: `\usepackage{lmodern}` in preamble if needed
- Check DPI setting (300 recommended for crispness)

### Figures Don't Execute
**Symptom:** Python figure code fails during extraction
**Solutions:**
- Ensure all imports from chapter are included in extracted code
- Check for dependencies on earlier code blocks
- Verify plotly and kaleido are installed for static export
- Run figure code independently to debug

### PowerPoint Layout Issues
**Symptom:** Content overlaps or doesn't fit on slides
**Solutions:**
- Adjust positioning in `build_presentation()` function
- Use custom reference template with `--theme` flag
- Modify slide layouts in python-pptx code
- Test with different content amounts per slide

### LaTeX Macros Not Recognized
**Symptom:** Custom commands like `\E`, `\d` cause rendering errors
**Solutions:**
- Script should automatically include macros.qmd content
- Verify preamble includes all `\newcommand` definitions
- Check that macros are valid LaTeX syntax

## Notes

This skill provides **fully automated** conversion from chapter QMD to presentation-ready PowerPoint with professional-quality LaTeX equations. No manual intervention required - the entire pipeline from source to slides is reproducible and scriptable.

**Key Advantages:**
- Production-quality LaTeX rendering (same as Beamer PDFs)
- Batch process all 16 chapters with one command
- Version control friendly (all outputs are generated files)
- Consistent formatting across all presentations
- Modify source chapter and regenerate slides instantly
