# Cover Image and Author Display Changes

## Date
2025-10-05

## Summary
Modified the book to display the cover image centered at the top of the home page with authors listed below it, instead of showing them in the YAML metadata.

## Files Modified

### 1. `_quarto.yml`
- **Removed**: Author metadata from the book section
  - Kerry Back, Rice University
  - Hong Liu, Washington University in St. Louis
  - Mark Loewenstein, University of Maryland

### 2. `index.qmd`
- **Added**: Cover image at the top of the page
  - Centered alignment
  - 50% width
- **Added**: Centered author list below the cover image
  - Kerry Back, Rice University
  - Hong Liu, Washington University in St. Louis
  - Mark Loewenstein, University of Maryland

### 3. `custom.css`
- **Added**: CSS rule to hide the book title text on the home page
  ```css
  /* Hide the book title text on home page (cover image is shown instead) */
  .quarto-title .title {
    display: none;
  }
  ```

## Rationale
- Eliminates redundancy between text title and cover image
- Provides better visual presentation with centered cover image
- Maintains proper HTML metadata while customizing visual display
- Authors appear more prominently below the cover image

## Technical Notes
- The text title "Pricing and Hedging Derivative Securities" remains in YAML for HTML metadata (SEO, accessibility)
- CSS hides the visual display of the title while keeping it in the document structure
- Cover image is responsive at 50% width
