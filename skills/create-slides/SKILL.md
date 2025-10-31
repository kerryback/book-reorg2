# Create Slides Skill

This skill creates professional presentation slides from chapter QMD files using a **two-stage pedagogical approach** for high-quality teaching materials.

## Overview

The skill converts chapter QMD files (e.g., `Chapter_ArbitragePricing.qmd`) into professional presentations suitable for teaching Masters of Finance students. The process prioritizes **pedagogical quality** over automation, creating slides with proper flow, motivation, and conceptual clarity.

## Two-Stage Workflow

### Stage 1: Create High-Quality Beamer Slides (Primary Output)

The first stage creates a pedagogically sound Beamer presentation that:

1. **Manual creation** of `Slides_[ChapterName].qmd` with Beamer format
2. **Pedagogical structure** designed for teaching:
   - Clear learning objectives
   - Motivation before concepts
   - Progressive builds and reveals
   - Examples and applications
   - Discussion questions
   - Key takeaways

3. **Render to PDF** using Quarto → Beamer → PDF pipeline

**Why Beamer First?**

- LaTeX math renders perfectly (native quality)
- Professional academic appearance
- Standard format for conference talks
- Excellent for projection and printing
- Full control over layout and typography

### Stage 2: Convert to PowerPoint (Optional, for Compatibility)

If PowerPoint format is needed:

1. **Export Beamer slides** to individual PNG images (one per slide)
2. **Extract LaTeX equations** from the QMD source
3. **Render equations to PNG** using matplotlib or similar
4. **Build PPTX** using python-pptx:
   - Import slide images as backgrounds
   - Overlay equation PNGs at appropriate positions
   - Add text boxes for editable content

## Detailed Workflow

### Step 1: Analyze Chapter Content

Read the chapter QMD file and identify:

- **Core concepts** that need explanation
- **Key equations** and their context
- **Examples** and applications
- **Difficult concepts** that need extra attention
- **Prerequisites** students need to know
- **Learning objectives** for the chapter

### Step 2: Design Pedagogical Structure

Create outline with proper teaching flow:

**Introduction (3-5 slides)**
- Learning objectives
- Motivation: Why does this matter?
- Connection to previous material
- Overview of what's coming

**Core Content (20-30 slides)**
- One concept per slide
- Intuition before formulas
- Build complexity gradually
- Examples after theory
- Visual aids and diagrams

**Applications (5-10 slides)**
- Practical uses
- Real-world examples
- Different solution methods
- When to use each approach

**Conclusion (3-5 slides)**
- Key takeaways
- Big picture summary
- Connection to next topic
- Discussion questions
- Additional resources

### Step 3: Write Beamer QMD File

Create `Slides_[ChapterName].qmd` with this structure:

```yaml
---
title: "Chapter Title"
subtitle: "Descriptive Subtitle"
author: "Finance 987"  # or course name
format:
  beamer:
    theme: Madrid
    colortheme: dolphin
    fonttheme: professionalfonts
    aspectratio: 169
    navigation: horizontal
    section-titles: true
    incremental: false
    toc: false
---

# Introduction

## Learning Objectives

By the end of this lecture, you will be able to:

- First objective
- Second objective
- Third objective

## Why Study This Topic?

**Key Insight:** Main motivation

. . .

This leads to:

- Important result 1
- Important result 2
- Important result 3

# Main Section 1

## First Concept

Explanation of concept...

. . .

**Key Formula:**
$$\text{important equation}$$

. . .

**Interpretation:** What does this mean?

## Example

Work through a concrete example...

# Key Takeaways

## Summary

Main points:

1. First takeaway
2. Second takeaway
3. Third takeaway

# Questions?

## Discussion

Think about:

1. Question 1
2. Question 2
```

### Step 4: Content Guidelines

**Slide Content Principles:**

- **One idea per slide**: Don't cram multiple concepts
- **Progressive disclosure**: Use `. . .` to build slides incrementally
- **Clear hierarchy**: Use headers, bold, and structure
- **Visual breathing room**: Don't fill every slide
- **Equations stand alone**: Give important equations their own slide
- **Examples after theory**: Don't mix derivations with applications

**Mathematical Content:**

- Introduce notation before using it
- Motivate equations before deriving them
- Explain economic/financial meaning
- Provide intuition, not just algebra
- Use concrete numbers in examples
- Show multiple solution methods when relevant

**Engagement Elements:**

- Discussion questions
- "Think about..." prompts
- Connections to current markets
- Historical context when relevant
- Common mistakes to avoid
- Practical tips for practitioners

### Step 5: Render Beamer PDF

```bash
quarto render Slides_[ChapterName].qmd
```

This creates `Slides_[ChapterName].pdf` with perfect LaTeX rendering.

**Quality checks:**

- [ ] All equations render correctly
- [ ] No slides too crowded (max 5-7 bullets)
- [ ] Progressive builds work properly
- [ ] Section transitions are clear
- [ ] Math notation is consistent
- [ ] Timing: 1.5-2 minutes per slide typical

### Step 6: (Optional) Convert to PowerPoint

If PowerPoint format is required, use this process:

#### 6a. Extract Slides as Images

Using pdf2image or similar:

```python
from pdf2image import convert_from_path

images = convert_from_path('Slides_[ChapterName].pdf', dpi=200)
for i, image in enumerate(images):
    image.save(f'slide_{i:03d}.png', 'PNG')
```

#### 6b. Extract and Render Equations

Parse the QMD source to extract equations:

```python
import re

with open('Slides_[ChapterName].qmd') as f:
    content = f.read()

# Extract display equations
equations = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)

# Render using matplotlib
import matplotlib.pyplot as plt

for i, eq in enumerate(equations):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.text(0.5, 0.5, f'${eq}$', fontsize=24, ha='center', va='center')
    ax.axis('off')
    plt.savefig(f'equation_{i:03d}.png', dpi=300, bbox_inches='tight',
                transparent=True)
    plt.close()
```

#### 6c. Build PowerPoint

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
prs.slide_width = Inches(13.33)  # 16:9 widescreen
prs.slide_height = Inches(7.5)

for i, slide_image in enumerate(slide_images):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # Add slide image as background
    left = Inches(0)
    top = Inches(0)
    pic = slide.shapes.add_picture(slide_image, left, top,
                                   width=prs.slide_width,
                                   height=prs.slide_height)

    # Move to back
    slide.shapes._spTree.remove(pic._element)
    slide.shapes._spTree.insert(2, pic._element)

prs.save('Slides_[ChapterName].pptx')
```

**Note:** This PowerPoint version is for compatibility only. The Beamer PDF is the primary high-quality output.

## Pedagogical Design Patterns

### Pattern 1: Concept Introduction

```
## [Concept Name]

**Definition:** Clear, concise definition

. . .

**Intuition:** Plain English explanation

. . .

**Key Properties:**
- Property 1
- Property 2
- Property 3
```

### Pattern 2: Equation Presentation

```
## [Equation Name]

**The Formula:**
$$\text{beautiful equation}$$

. . .

**Where:**
- $x$ = first variable
- $y$ = second variable

. . .

**Economic Meaning:** What does this tell us?
```

### Pattern 3: Example Structure

```
## Example: [Scenario]

**Given:**
- Parameter 1 = value
- Parameter 2 = value

. . .

**Find:** What we're looking for

. . .

**Solution:**
1. Step 1
2. Step 2
3. Answer
```

### Pattern 4: Comparison Slides

```
## Three Methods to Price

**Method 1: [Name]**
- When to use: ...
- Advantage: ...

. . .

**Method 2: [Name]**
- When to use: ...
- Advantage: ...

. . .

**Method 3: [Name]**
- When to use: ...
- Advantage: ...
```

### Pattern 5: Takeaway Slides

```
## Key Takeaways

::: {.block}
### Main Result

Clear statement of the most important point
:::

. . .

**Practical Implications:**
- Implication 1
- Implication 2
```

## Example: Creating Slides for Arbitrage Pricing Chapter

### Step 1: Analysis

The chapter covers:
- Linear pricing foundations
- State prices and Arrow securities
- Risk-neutral probabilities
- Change of numeraire
- Fundamental pricing formula

**Key teaching challenges:**
- Why risk-neutral probabilities work (they're not "real")
- Change of numeraire seems arbitrary
- Connection between discrete and continuous time

### Step 2: Pedagogical Structure

**Introduction:**
1. Learning objectives
2. Why study arbitrage pricing? (connects everything)
3. Intuition: "no free lunch"

**Core Content:**
1. Linear pricing (start with fruit example)
2. State prices (concrete binomial model first)
3. Arrow securities (building block concept)
4. Risk-neutral probabilities (why they work)
5. Multiple states (generalization)
6. Continuous time (SDFs)
7. Change of numeraire (motivation first!)
8. Stock as numeraire (applications)
9. Girsanov's theorem (intuition only)

**Applications:**
1. Three methods to price same option
2. When to use each method

**Conclusion:**
1. Big picture summary
2. Practical implications
3. Connection to Black-Scholes

### Step 3: Implementation

See `Slides_ArbitragePricing.qmd` for complete example with:
- 40+ slides with proper pacing
- Progressive reveals for complex concepts
- Clear mathematical notation
- Conceptual explanations before formulas
- Multiple examples
- Discussion questions

## Quality Standards

### Content Quality

- [ ] Clear learning objectives stated upfront
- [ ] Motivation provided before diving into math
- [ ] One main idea per slide
- [ ] Progressive builds for complex concepts
- [ ] Examples follow theory
- [ ] Economic/financial intuition provided
- [ ] Common mistakes addressed
- [ ] Practical applications shown

### Visual Quality

- [ ] Consistent fonts and colors
- [ ] Adequate white space
- [ ] Readable from back of room (min 18pt font)
- [ ] Equations clearly visible
- [ ] No slide too crowded (max 5-7 bullets)
- [ ] Section transitions clear

### Teaching Quality

- [ ] Appropriate pace (1.5-2 min per slide)
- [ ] Engagement elements included
- [ ] Discussion questions provided
- [ ] Builds on prior knowledge
- [ ] Previews what's coming next
- [ ] Suitable for target audience (Masters students)

## Tools and Dependencies

**Required:**
- Quarto (for rendering Beamer)
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Python 3.8+ (for optional PPTX conversion)

**Optional (for PPTX conversion):**
- python-pptx: `pip install python-pptx`
- matplotlib: `pip install matplotlib`
- pdf2image: `pip install pdf2image`
- Pillow: `pip install Pillow`

## Usage

### Creating Beamer Slides (Primary Workflow)

1. Read the chapter QMD file thoroughly
2. Identify key concepts and teaching challenges
3. Design pedagogical structure with proper flow
4. Create `Slides_[ChapterName].qmd` by hand with care
5. Render with `quarto render Slides_[ChapterName].qmd`
6. Review PDF and iterate on content

**Time estimate:** 2-4 hours for a comprehensive chapter

### Converting to PowerPoint (Optional)

Only do this if PowerPoint format is specifically required:

```bash
python beamer_to_pptx.py Slides_[ChapterName].pdf
```

This creates `Slides_[ChapterName].pptx` with:
- Each slide as an image background
- Equations as overlaid PNGs
- Editable text boxes where appropriate

## Best Practices

### Do's

✅ Start with motivation and learning objectives
✅ Use progressive builds (`. . .`) for complex ideas
✅ Provide intuition before formulas
✅ Include concrete examples with numbers
✅ Show multiple solution methods when relevant
✅ End with key takeaways and discussion
✅ Keep slides focused and uncluttered
✅ Test timing (1.5-2 min per slide)

### Don'ts

❌ Don't cram multiple concepts per slide
❌ Don't show derivations without motivation
❌ Don't use tiny fonts (min 18pt)
❌ Don't skip examples
❌ Don't forget to explain notation
❌ Don't use jargon without definition
❌ Don't rush through key equations
❌ Don't forget to connect to big picture

## Common Patterns for Finance Topics

### Pricing Formula Introduction

1. Motivation: Why do we need this formula?
2. Setup: What are the assumptions?
3. Intuition: What's the economic idea?
4. Formula: Show the math
5. Interpretation: What does each term mean?
6. Example: Calculate with real numbers
7. Application: When do we use this?

### Proof or Derivation

1. State the result clearly first
2. Explain why it's important
3. Show key steps only (not every line)
4. Emphasize the main insight
5. Verify with an example
6. Discuss when it applies

### Model Comparison

1. Setup: Common problem to solve
2. Method 1: Explain and show
3. Method 2: Explain and show
4. Method 3: Explain and show
5. Comparison: When to use each?
6. Example: Apply all three methods

## Summary

**Primary Output:** High-quality Beamer PDF slides created manually with pedagogical care

**Optional Secondary Output:** PowerPoint PPTX for compatibility

**Key Principle:** Content quality over automation. Each chapter deserves thoughtful slide design that prioritizes student learning.

**Expected Result:** Professional academic slides suitable for teaching Masters of Finance courses, with perfect LaTeX rendering, clear pedagogical flow, and appropriate pacing.
