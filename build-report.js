const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak, TabStopType, TabStopPosition } = require('docx');
const fs = require('fs');

// ─── CONSTANTS ───
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CONTENT_W = PAGE_W - MARGIN * 2; // 9360
const GREEN = "1D9E75";
const DARK = "1A1A1A";
const GRAY = "6B6B6B";
const LIGHT_GRAY = "F7F7F5";
const BORDER_COLOR = "D0D0D0";

const border = { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

// ─── HELPERS ───
function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, bold: true, size: 32, font: "Arial", color: DARK })] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, bold: true, size: 26, font: "Arial", color: DARK })] });
}
function h3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, bold: true, size: 22, font: "Arial", color: GREEN })] });
}
function p(text, opts = {}) {
  return new Paragraph({ spacing: { after: 120 },
    children: [new TextRun({ text, size: 20, font: "Arial", color: opts.color || GRAY, bold: opts.bold, italics: opts.italic })] });
}
function bold(text) { return p(text, { bold: true, color: DARK }); }

function bulletItem(text, ref) {
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 },
    children: [new TextRun({ text, size: 20, font: "Arial", color: GRAY })] });
}

function tableRow(cells, isHeader = false) {
  return new TableRow({
    children: cells.map((text, i) => {
      const widths = cells.length === 4 ? [2800, 2200, 2200, 2160] :
                     cells.length === 3 ? [3500, 3000, 2860] :
                     cells.length === 5 ? [2800, 1400, 1400, 1400, 2360] :
                     cells.length === 2 ? [4000, 5360] : [CONTENT_W / cells.length];
      return new TableCell({
        borders, width: { size: widths[i] || 2000, type: WidthType.DXA },
        margins: cellMargins,
        shading: isHeader ? { fill: GREEN, type: ShadingType.CLEAR } : { fill: "FFFFFF", type: ShadingType.CLEAR },
        children: [new Paragraph({
          children: [new TextRun({ text: String(text), size: 18, font: "Arial", bold: isHeader, color: isHeader ? "FFFFFF" : DARK })]
        })]
      });
    })
  });
}

function makeTable(headers, rows, colWidths) {
  const widths = colWidths || (headers.length === 4 ? [2800, 2200, 2200, 2160] :
    headers.length === 3 ? [3500, 3000, 2860] :
    headers.length === 5 ? [2800, 1400, 1400, 1400, 2360] :
    headers.length === 2 ? [4000, 5360] :
    Array(headers.length).fill(Math.floor(CONTENT_W / headers.length)));
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      tableRow(headers, true),
      ...rows.map(r => tableRow(r))
    ]
  });
}

function spacer() { return new Paragraph({ spacing: { after: 200 }, children: [] }); }
function pageBreak() { return new Paragraph({ children: [new PageBreak()] }); }

// ─── BUILD DOCUMENT ───
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Arial", color: GREEN },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets2", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets3", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [
    // ════════════════════════ COVER PAGE ════════════════════════
    {
      properties: {
        page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } }
      },
      children: [
        spacer(), spacer(), spacer(), spacer(), spacer(),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
          children: [new TextRun({ text: "KINBIRD PRO", size: 20, font: "Arial", color: GREEN, bold: true, characterSpacing: 300 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
          children: [new TextRun({ text: "Deep Competitive Research Report", size: 48, font: "Arial", color: DARK, bold: true })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({ text: "BirdTracks.io Analysis", size: 28, font: "Arial", color: GRAY })] }),
        spacer(),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
          children: [new TextRun({ text: "Prepared for Ayaan Ahmed Shohan", size: 22, font: "Arial", color: GRAY })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
          children: [new TextRun({ text: "Founder, KinBird Aviary", size: 20, font: "Arial", color: GRAY })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({ text: "June 2026", size: 20, font: "Arial", color: GRAY })] }),
        spacer(), spacer(),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
          border: { top: { style: BorderStyle.SINGLE, size: 2, color: GREEN } },
          children: [] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
          children: [new TextRun({ text: "\"Learn from everything. Copy nothing. Build something better.\"", size: 20, font: "Arial", color: GREEN, italics: true })] }),
      ]
    },
    // ════════════════════════ EXECUTIVE SUMMARY ════════════════════════
    {
      properties: {
        page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } }
      },
      headers: {
        default: new Header({ children: [new Paragraph({
          children: [new TextRun({ text: "KinBird Pro — BirdTracks Competitive Research", size: 16, font: "Arial", color: GRAY, italics: true })],
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }]
        })] })
      },
      footers: {
        default: new Footer({ children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Page ", size: 16, font: "Arial", color: GRAY }), new TextRun({ children: [PageNumber.CURRENT], size: 16, font: "Arial", color: GRAY })]
        })] })
      },
      children: [
        h1("Executive Summary"),
        p("BirdTracks is the most mature bird breeding SaaS currently available, serving global breeders with a feature-rich platform covering bird management, breeding pairs, cage tracking, genetics, and financial reporting. After conducting a thorough page-by-page analysis of every major BirdTracks screen, this report identifies critical competitive intelligence for KinBird Pro."),
        spacer(),
        bold("Key Findings:"),
        bulletItem("BirdTracks excels in genetics/offspring prediction, bulk data import, and cage QR workflows — areas KinBird must address", "bullets"),
        bulletItem("KinBird Pro already leads in UX quality, mobile-first design, modern SaaS aesthetics, and empty state design patterns", "bullets"),
        bulletItem("BirdTracks’ pricing model (8-day trial, 10-bird limit, milestone extensions) reveals effective conversion mechanics worth studying", "bullets"),
        bulletItem("Their purple/gradient design language feels dated compared to KinBird’s Linear/Stripe-inspired clean aesthetic", "bullets"),
        bulletItem("BirdTracks uses “—” dashes for empty data everywhere — KinBird’s CTA-driven empty states are categorically superior", "bullets"),
        bulletItem("Their Stats page (COI, genetic diversity) is paywalled behind Breeder tier — KinBird can democratize basic analytics", "bullets"),

        spacer(),
        bold("Overall BirdTracks Score:"),
        makeTable(
          ["Dimension", "Score /100"],
          [
            ["UX Quality", "62"],
            ["Mobile Experience", "55"],
            ["Feature Completeness", "82"],
            ["Speed / Performance", "68"],
            ["Breeder Friendliness", "73"],
            ["Design & Aesthetics", "45"],
            ["Data Architecture", "78"],
            ["Overall Weighted", "66"],
          ],
          [5000, 4360]
        ),

        pageBreak(),

        // ════════════════════════ PAGE-BY-PAGE ANALYSIS ════════════════════════
        h1("Page-by-Page Analysis"),

        // ── BIRDS LIST ──
        h2("1. Birds List (/birds)"),
        h3("Purpose"),
        p("Central hub for browsing, searching, filtering, and managing the entire bird portfolio. Serves as the primary entry point for breeders."),
        h3("Strengths"),
        bulletItem("Comprehensive filter system: species, sex, status, mutation, availability, cage assignment", "bullets2"),
        bulletItem("Quick search bar with instant results", "bullets2"),
        bulletItem("Bulk actions available (select multiple birds)", "bullets2"),
        bulletItem("\"Paste from Spreadsheet\" import — genius onboarding feature for breeders migrating from Excel", "bullets2"),
        bulletItem("Status badges clearly indicate bird state (Active, For Sale, Deceased, etc.)", "bullets2"),
        h3("Weaknesses"),
        bulletItem("No gallery/grid view — table-only display feels data-heavy for visual breeders", "bullets2"),
        bulletItem("Generic Twitter bird silhouette as photo placeholder — unbranded and uninspiring", "bullets2"),
        bulletItem("Purple gradient color scheme looks dated against modern SaaS standards", "bullets2"),
        bulletItem("Mobile experience cramped — table rows too dense for thumb navigation", "bullets2"),
        bulletItem("No quick-preview/popup — must navigate to full profile for basic info", "bullets2"),
        h3("KinBird Advantage"),
        p("KinBird’s dual Table + Gallery view already superior. Our sex-tinted placeholder images (blue/pink/neutral) are more branded. Quick-action popups eliminate unnecessary navigation. Mobile card layout > cramped table rows."),
        h3("Score"),
        makeTable(["Metric", "Score"], [["UX", "60"], ["Mobile", "48"], ["Speed", "70"], ["Discoverability", "72"], ["Power User", "65"], ["Breeder Friendliness", "68"]], [5000, 4360]),

        pageBreak(),

        // ── ADD BIRD ──
        h2("2. Add Bird (/birds/new)"),
        h3("Strengths"),
        bulletItem("Mandatory fields kept minimal: Species + Band ID only required", "bullets3"),
        bulletItem("Optional fields organized in collapsible sections (Identity, Physical, Acquisition)", "bullets3"),
        bulletItem("\"Paste from Spreadsheet\" tab for bulk import — extremely valuable for onboarding", "bullets3"),
        bulletItem("Parent linking with search dropdown (Dam/Sire fields)", "bullets3"),
        bulletItem("Photo upload with drag-and-drop", "bullets3"),
        h3("Weaknesses"),
        bulletItem("Form layout is single-column, long scroll — wastes horizontal space on desktop", "bullets3"),
        bulletItem("No inline validation — errors only shown on submit", "bullets3"),
        bulletItem("No \"quick add\" mode for rapid data entry during breeding season", "bullets3"),
        bulletItem("Mutation field is free-text, not dropdown from species-specific mutations", "bullets3"),
        h3("KinBird Opportunity"),
        p("Implement: (1) Two-column form on desktop, (2) Smart mutation dropdown per species, (3) Quick-add mode with minimal fields + keyboard shortcuts, (4) CSV/Spreadsheet import equivalent. Priority: Spreadsheet import is a must-have for onboarding."),
        h3("Score"),
        makeTable(["Metric", "Score"], [["UX", "64"], ["Mobile", "58"], ["Speed", "72"], ["Efficiency", "60"], ["Breeder Friendliness", "70"]], [5000, 4360]),

        pageBreak(),

        // ── BIRD PROFILE ──
        h2("3. Bird Profile"),
        h3("Strengths"),
        bulletItem("Comprehensive data display: identity, genetics, lineage, breeding history, offspring", "bullets"),
        bulletItem("Pedigree tree view (3-generation) embedded in profile", "bullets"),
        bulletItem("Offspring Predictions with genetic percentages — killer feature KinBird lacks", "bullets"),
        bulletItem("Quick action buttons: Edit, Transfer, Mark Deceased, Print Label", "bullets"),
        bulletItem("Related birds section (siblings, offspring) with clickable links", "bullets"),
        h3("Weaknesses"),
        bulletItem("Dense information hierarchy — no clear visual grouping", "bullets"),
        bulletItem("\"---\" dashes for every empty field instead of contextual CTAs", "bullets"),
        bulletItem("Photo area uses generic silhouette — no sex-tinted variants", "bullets"),
        bulletItem("No timeline/activity log for the bird’s life events", "bullets"),
        bulletItem("Mobile scrolling is excessive due to no accordion/tab pattern", "bullets"),
        h3("KinBird Advantage"),
        p("KinBird’s v3 bird profile already uses icon rows, grouped sections, and CTA-driven empty states. Our visual hierarchy is cleaner. We need to ADD: offspring prediction engine, pedigree tree, and life event timeline. But the UX wrapper is already better."),
        h3("Score"),
        makeTable(["Metric", "Score"], [["UX", "65"], ["Mobile", "52"], ["Data Density", "80"], ["Visual Hierarchy", "55"], ["Breeder Friendliness", "75"]], [5000, 4360]),

        pageBreak(),

        // ── CAGES ──
        h2("4. Cages (/cages)"),
        h3("Strengths"),
        bulletItem("Grid layout with cage cards showing occupancy count", "bullets2"),
        bulletItem("QR code generation per cage — print labels for physical walk-throughs", "bullets2"),
        bulletItem("Capacity management: max birds per cage setting", "bullets2"),
        bulletItem("Color-coded status indicators", "bullets2"),
        h3("Weaknesses"),
        bulletItem("No visual floor plan / spatial layout view", "bullets2"),
        bulletItem("QR scanning workflow requires external app — not built into BirdTracks mobile", "bullets2"),
        bulletItem("No cage history (which birds were in this cage over time)", "bullets2"),
        bulletItem("Limited filtering options", "bullets2"),
        h3("KinBird Opportunity"),
        p("Build cage management with: (1) QR code generation + in-app scanner via Capacitor camera API, (2) Cage history timeline, (3) Visual floor plan view (drag-and-drop cage arrangement). The QR workflow should be fully native — no external app needed."),
        h3("Score"),
        makeTable(["Metric", "Score"], [["UX", "62"], ["Mobile", "55"], ["Utility", "70"], ["Breeder Friendliness", "72"]], [5000, 4360]),

        pageBreak(),

        // ── CAGE DETAIL ──
        h2("5. Cage Detail"),
        h3("Strengths"),
        bulletItem("\"Scan Next Cage\" button — brilliant for physical aviary walk-throughs", "bullets3"),
        bulletItem("Birds in cage listed with quick links", "bullets3"),
        bulletItem("Active pair displayed if cage is a breeding cage", "bullets3"),
        bulletItem("Clutch information visible at cage level", "bullets3"),
        h3("Weaknesses"),
        bulletItem("Sparse layout — lots of empty space with minimal data", "bullets3"),
        bulletItem("No environmental data fields (temperature, humidity, light cycle)", "bullets3"),
        bulletItem("No maintenance log or cleaning schedule", "bullets3"),
        h3("KinBird Opportunity"),
        p("Add environmental tracking fields, maintenance schedule, and a \"walk-through mode\" that sequences through cages with swipe gestures. The scan-next pattern is worth adopting but should feel native on mobile."),

        pageBreak(),

        // ── PAIRS ──
        h2("6. Pairs (/pairs)"),
        h3("Strengths"),
        bulletItem("Clear Male + Female display per pair row", "bullets"),
        bulletItem("Clutch count and success rate visible in list", "bullets"),
        bulletItem("Filter by active/inactive/all pairs", "bullets"),
        bulletItem("Quick pair creation workflow", "bullets"),
        h3("Weaknesses"),
        bulletItem("Hatch Rate shows \"---\" when no data — classic BirdTracks empty state problem", "bullets"),
        bulletItem("No genetic compatibility indicator before pairing", "bullets"),
        bulletItem("No \"suggested pairs\" feature based on genetics", "bullets"),
        bulletItem("Performance metrics buried in detail page, not visible in list", "bullets"),
        h3("KinBird Advantage"),
        p("KinBird should show: (1) Genetic compatibility score before pairing (green/yellow/red), (2) Suggested pairs engine based on mutation goals + COI, (3) Quick-stats in list view (clutches, avg chicks, hatch rate). The mutation predictor is a moat feature."),

        pageBreak(),

        // ── PAIR DETAIL ──
        h2("7. Pair Detail"),
        h3("Strengths"),
        bulletItem("Complete breeding history with clutch timeline", "bullets2"),
        bulletItem("Offspring listed per clutch with status", "bullets2"),
        bulletItem("Egg tracking: laid date, fertile/infertile, hatch date", "bullets2"),
        bulletItem("KPIs: total eggs, total hatched, fertility rate", "bullets2"),
        h3("Weaknesses"),
        bulletItem("Data-heavy layout with poor visual hierarchy", "bullets2"),
        bulletItem("No visual timeline — just tables", "bullets2"),
        bulletItem("Offspring prediction not linked to pair context", "bullets2"),
        bulletItem("No \"pair health\" dashboard (rest periods, overbreeding alerts)", "bullets2"),
        h3("KinBird Opportunity"),
        p("Build a visual breeding timeline (horizontal scrolling clutch cards). Add pair health monitoring: alert if pair has had >3 consecutive clutches without rest, flag declining fertility trends, and integrate offspring mutation predictions directly into pair detail."),

        pageBreak(),

        // ── CALENDAR ──
        h2("8. Calendar (/calendar)"),
        h3("Strengths"),
        bulletItem("Daily view of breeding events: eggs expected to hatch, weaning dates, pair events", "bullets3"),
        bulletItem("Reminder system for time-sensitive breeding tasks", "bullets3"),
        bulletItem("Color-coded event types", "bullets3"),
        bulletItem("Breeding calendar for planning future pairings", "bullets3"),
        h3("Weaknesses"),
        bulletItem("Monthly view only — no week or day view", "bullets3"),
        bulletItem("No push notifications — only in-app reminders", "bullets3"),
        bulletItem("Cannot set custom recurring events", "bullets3"),
        bulletItem("Events not draggable/reschedulable", "bullets3"),
        h3("KinBird Opportunity"),
        p("Build with: (1) Push notifications via Capacitor for hatch day alerts, (2) Week/day/month views, (3) Auto-generated events from egg data (\"Day 18 — candling due\", \"Day 23 — expected hatch\"), (4) Integrate with phone calendar for cross-app visibility."),

        pageBreak(),

        // ── SETTINGS ──
        h2("9. Settings (/settings)"),
        h3("Key Intelligence"),
        bulletItem("Free Trial: 8 days OR 10 birds (whichever comes first)", "bullets"),
        bulletItem("Milestone-based trial extensions: complete profile = +2 days, add first bird = +3 days, etc.", "bullets"),
        bulletItem("Referral program: refer a breeder = extend trial", "bullets"),
        bulletItem("Tiered pricing: Basic, Standard, Breeder (COI/Stats locked to Breeder tier)", "bullets"),
        bulletItem("Species selection during onboarding restricts available mutations", "bullets"),
        h3("Weaknesses"),
        bulletItem("Cluttered settings page with too many sections", "bullets"),
        bulletItem("No dark mode toggle (OS-level only)", "bullets"),
        bulletItem("Limited customization of bird fields/categories", "bullets"),
        h3("KinBird Opportunity"),
        p("Adopt the milestone-based trial extension model — it drives activation. But democratize basic analytics (give COI calculator to all tiers, paywall only advanced genetics). Settings should be clean, grouped, with search."),

        pageBreak(),

        // ── STATS ──
        h2("10. Stats Page"),
        h3("Strengths"),
        bulletItem("COI (Coefficient of Inbreeding) calculator — critical for serious breeders", "bullets2"),
        bulletItem("Genetic diversity metrics", "bullets2"),
        bulletItem("Flock statistics: total birds, sex ratio, species breakdown", "bullets2"),
        bulletItem("Financial reports (paywalled)", "bullets2"),
        h3("Weaknesses"),
        bulletItem("Entirely paywalled behind Breeder tier — no preview to drive upgrades", "bullets2"),
        bulletItem("Basic stats (bird count, sex ratio) should be free", "bullets2"),
        bulletItem("No visual charts — just numbers", "bullets2"),
        bulletItem("No export functionality", "bullets2"),
        h3("KinBird Opportunity"),
        p("Give basic stats (count, ratio, mortality rate) to all users. Paywall advanced genetics (COI, diversity index, prediction engine). Always show charts, not just numbers. Add export to PDF/Excel for breeders who need reports for bird associations."),

        pageBreak(),

        // ════════════════════════ FEATURE GAP ANALYSIS ════════════════════════
        h1("Feature Gap Analysis"),
        p("Comprehensive comparison of features across both platforms. Winner determined by implementation quality, not just presence."),
        spacer(),
        makeTable(
          ["Feature", "BirdTracks", "KinBird Pro", "Winner"],
          [
            ["Bird Portfolio List", "Table only, filters", "Table + Gallery + Popup", "KinBird"],
            ["Bird Profile Page", "Dense, data-rich", "Icon rows, grouped sections", "KinBird"],
            ["Add Bird Form", "Long single-column", "Multi-step, smart fields", "KinBird"],
            ["Photo Placeholder", "Generic Twitter bird", "Sex-tinted branded SVG", "KinBird"],
            ["Empty State Design", "\"---\" dashes everywhere", "CTA-driven empty states", "KinBird"],
            ["Visual Design", "Purple gradients, dated", "Linear/Stripe modern", "KinBird"],
            ["Mobile UX", "Cramped tables", "Mobile-first cards", "KinBird"],
            ["Spreadsheet Import", "Paste from clipboard", "Not yet built", "BirdTracks"],
            ["Offspring Predictions", "Genetic % calculator", "Not yet built", "BirdTracks"],
            ["Pedigree Tree", "3-gen embedded", "Not yet built", "BirdTracks"],
            ["QR Code Labels", "Generate + print", "Not yet built", "BirdTracks"],
            ["Cage Management", "Grid + QR scan", "Not yet built", "BirdTracks"],
            ["Breeding Calendar", "Monthly + reminders", "Not yet built", "BirdTracks"],
            ["COI Calculator", "Paywalled", "Not yet built", "BirdTracks"],
            ["Financial Reports", "Paywalled", "Sales module planned", "Tie"],
            ["Push Notifications", "None (in-app only)", "Capacitor native (planned)", "KinBird (planned)"],
            ["Dark Mode", "OS-level only", "Full CSS variable system", "KinBird"],
            ["Bangla Language", "No", "Native Hind Siliguri", "KinBird"],
            ["Breeder Marketplace", "Not available", "D3 Sales module", "KinBird"],
            ["Customer Dashboard", "Not available", "D4 planned", "KinBird"],
            ["Referral System", "Trial extension", "Not yet built", "BirdTracks"],
            ["Trial Onboarding", "Milestone extensions", "Not yet designed", "BirdTracks"],
            ["Bulk Actions", "Select + batch", "Quick actions per bird", "Tie"],
            ["Scan Next Cage", "Physical walk-through", "Not yet built", "BirdTracks"],
          ]
        ),

        pageBreak(),

        // ════════════════════════ UX GAP ANALYSIS ════════════════════════
        h1("UX Gap Analysis"),

        h2("Where KinBird Wins"),
        bulletItem("Modern SaaS aesthetic (Linear/Stripe/Framer influence) vs BirdTracks’ dated purple gradients", "bullets"),
        bulletItem("Mobile-first card layouts vs cramped desktop-first tables", "bullets"),
        bulletItem("CTA-driven empty states (“Add your first bird”) vs unhelpful “---” dashes", "bullets"),
        bulletItem("Sex-tinted photo placeholders (blue/pink/neutral) vs generic silhouette", "bullets"),
        bulletItem("Icon row data display vs dense text blocks", "bullets"),
        bulletItem("Quick-action popup modals vs full page navigation for simple tasks", "bullets"),
        bulletItem("Grouped sections with visual hierarchy vs flat information dumps", "bullets"),
        bulletItem("Native Bangla support for Bangladesh market", "bullets"),
        bulletItem("Dark mode with full CSS variable system", "bullets"),
        bulletItem("44px minimum touch targets enforced system-wide", "bullets"),

        spacer(),
        h2("Where BirdTracks Wins"),
        bulletItem("Genetics engine: offspring predictions with mutation percentages", "bullets2"),
        bulletItem("Bulk data onboarding: paste-from-spreadsheet import", "bullets2"),
        bulletItem("Physical-to-digital bridge: QR codes + cage scanning workflow", "bullets2"),
        bulletItem("Breeding calendar with automated event generation", "bullets2"),
        bulletItem("Pedigree tree visualization (3 generations)", "bullets2"),
        bulletItem("Milestone-based trial extension (gamified onboarding)", "bullets2"),
        bulletItem("Comprehensive statistics page (even if paywalled)", "bullets2"),
        bulletItem("Scan Next Cage sequential walk-through pattern", "bullets2"),
        bulletItem("Mature referral program for organic growth", "bullets2"),

        spacer(),
        h2("Net Assessment"),
        p("KinBird leads on UX quality and design execution. BirdTracks leads on feature breadth and breeding-specific workflows. The gap is closable: KinBird’s superior foundation means each new feature will be better implemented than BirdTracks’ equivalent. The priority is adding the missing features without compromising the UX advantage."),

        pageBreak(),

        // ════════════════════════ TOP 50 PRODUCT IDEAS ════════════════════════
        h1("Top 50 Product Ideas"),
        p("Ranked by Impact (1–10) × Breeder Value (1–10) / Difficulty (1–10). Higher composite = build first."),
        spacer(),
        makeTable(
          ["#", "Idea", "Impact", "Difficulty", "Priority"],
          [
            ["1", "Offspring Mutation Predictor (genetics engine)", "10", "8", "Critical"],
            ["2", "Paste-from-Spreadsheet bulk import", "9", "4", "Critical"],
            ["3", "Pedigree tree visualization (3-gen)", "9", "6", "Critical"],
            ["4", "Breeding Calendar with auto events", "9", "6", "Critical"],
            ["5", "Push notifications (hatch alerts, reminders)", "8", "4", "Critical"],
            ["6", "COI calculator (free tier basic)", "8", "7", "High"],
            ["7", "QR code cage labels + in-app scanner", "8", "5", "High"],
            ["8", "CSV/Excel export for all data", "7", "3", "High"],
            ["9", "Milestone-based trial onboarding", "8", "4", "High"],
            ["10", "Genetic compatibility score (pair creation)", "9", "7", "High"],
            ["11", "Suggested pairs engine (mutation goals)", "9", "8", "High"],
            ["12", "Bird life event timeline", "7", "4", "High"],
            ["13", "Pair health monitoring (overbreeding alerts)", "8", "5", "High"],
            ["14", "Cage history timeline", "6", "3", "Medium"],
            ["15", "Flock analytics dashboard (charts)", "7", "5", "Medium"],
            ["16", "Mortality rate tracking + alerts", "7", "4", "Medium"],
            ["17", "Egg candling reminders (auto Day 7/14/18)", "8", "3", "High"],
            ["18", "Referral system for organic growth", "7", "5", "Medium"],
            ["19", "Breeder community forum/feed", "6", "7", "Medium"],
            ["20", "Dark mode toggle in settings", "5", "2", "Medium"],
            ["21", "Cage walk-through mode (swipe between cages)", "6", "4", "Medium"],
            ["22", "Bird comparison tool (side-by-side)", "6", "4", "Medium"],
            ["23", "Breeding season planner", "7", "5", "Medium"],
            ["24", "Expense tracking per bird/pair", "7", "5", "Medium"],
            ["25", "Revenue per bird analytics", "7", "4", "Medium"],
            ["26", "Photo gallery per bird (multiple images)", "6", "3", "Medium"],
            ["27", "Weight/health tracking log", "7", "4", "Medium"],
            ["28", "Medication/treatment log", "7", "4", "Medium"],
            ["29", "Breeder certification badges", "5", "3", "Low"],
            ["30", "PDF bird certificates (printable)", "6", "4", "Medium"],
            ["31", "Clutch success rate analytics", "7", "4", "Medium"],
            ["32", "Auto-archive deceased birds after X days", "4", "2", "Low"],
            ["33", "Duplicate bird detection (band ID)", "5", "3", "Medium"],
            ["34", "Custom fields (user-defined attributes)", "6", "6", "Medium"],
            ["35", "Bird transfer between breeders", "6", "5", "Medium"],
            ["36", "Breeding contract templates", "5", "4", "Low"],
            ["37", "Buyer messaging system", "6", "6", "Medium"],
            ["38", "Public breeder profile page", "7", "5", "Medium"],
            ["39", "Instagram-style share cards for birds", "6", "4", "Medium"],
            ["40", "Inventory management (food, supplies)", "5", "5", "Low"],
            ["41", "Weather integration for breeding conditions", "4", "4", "Low"],
            ["42", "Bird DNA test result storage", "6", "3", "Medium"],
            ["43", "Breeding pair rotation scheduler", "6", "5", "Medium"],
            ["44", "Multi-aviary support (locations)", "6", "5", "Medium"],
            ["45", "Staff/helper access roles", "5", "5", "Low"],
            ["46", "Offline mode (Capacitor)", "7", "7", "Medium"],
            ["47", "Voice note attachments per bird", "4", "4", "Low"],
            ["48", "Smart search (natural language)", "5", "6", "Low"],
            ["49", "Annual breeding report generator", "6", "5", "Medium"],
            ["50", "WhatsApp share integration", "7", "3", "High"],
          ],
          [400, 5160, 1000, 1200, 1600]
        ),

        pageBreak(),

        // ════════════════════════ KINBIRD ROADMAP ════════════════════════
        h1("KinBird Pro Roadmap"),
        p("Based on competitive analysis. Organized by timeframe and strategic priority."),

        h2("Immediate (Weeks 1–3)"),
        p("Ship these to close the most critical feature gaps:"),
        bulletItem("Paste-from-Spreadsheet import (onboarding blocker)", "bullets3"),
        bulletItem("Push notifications via Capacitor (hatch alerts)", "bullets3"),
        bulletItem("CSV/Excel export for all data views", "bullets3"),
        bulletItem("Milestone-based trial onboarding flow", "bullets3"),
        bulletItem("Egg candling auto-reminders (Day 7/14/18)", "bullets3"),
        bulletItem("WhatsApp share integration for bird listings", "bullets3"),

        h2("Short-Term (Weeks 4–8)"),
        p("Build the breeding intelligence features that create competitive moat:"),
        bulletItem("Offspring Mutation Predictor engine", "bullets"),
        bulletItem("Pedigree tree visualization (3-gen)", "bullets"),
        bulletItem("Breeding Calendar with auto-generated events", "bullets"),
        bulletItem("COI calculator (basic free, advanced paid)", "bullets"),
        bulletItem("Genetic compatibility score for pair creation", "bullets"),
        bulletItem("QR code cage labels + in-app scanner", "bullets"),
        bulletItem("Pair health monitoring + overbreeding alerts", "bullets"),
        bulletItem("Bird life event timeline", "bullets"),
        bulletItem("Flock analytics dashboard with charts", "bullets"),

        h2("Long-Term (Months 3–6)"),
        p("Build the moat features that make KinBird irreplaceable:"),
        bulletItem("Suggested pairs engine (AI-driven based on mutation goals + COI)", "bullets2"),
        bulletItem("Breeder marketplace (D3 Sales fully operational)", "bullets2"),
        bulletItem("Customer dashboard with delivery tracking (D4)", "bullets2"),
        bulletItem("Public breeder profile pages", "bullets2"),
        bulletItem("Referral system for organic growth", "bullets2"),
        bulletItem("Multi-aviary support", "bullets2"),
        bulletItem("Offline mode via Capacitor", "bullets2"),
        bulletItem("Annual breeding report generator (PDF export)", "bullets2"),
        bulletItem("Breeder community features", "bullets2"),

        pageBreak(),

        // ════════════════════════ FOUNDER RECOMMENDATION ════════════════════════
        h1("Founder Recommendation"),
        p("If I were building KinBird Pro from scratch today, after studying BirdTracks extensively, here is what I would do:"),

        spacer(),
        h2("What I Would Keep"),
        bulletItem("KinBird’s mobile-first, Linear/Stripe design language — it’s categorically better than BirdTracks’ dated aesthetic", "bullets"),
        bulletItem("CTA-driven empty states (never show \"---\" dashes)", "bullets"),
        bulletItem("Icon row data patterns for bird profiles", "bullets"),
        bulletItem("Quick-action popup modals (avoid full-page navigations for simple tasks)", "bullets"),
        bulletItem("Native Bangla support — this is a market advantage BirdTracks cannot match", "bullets"),
        bulletItem("The D1-D4 module architecture (Portfolio → Production → Sales → Customers) — this end-to-end flow is unique", "bullets"),
        bulletItem("Sex-tinted placeholder images and branded design system", "bullets"),
        bulletItem("Supabase + Next.js + Capacitor tech stack — correct for the scale and market", "bullets"),

        spacer(),
        h2("What I Would Do Differently"),
        bulletItem("Ship the mutation predictor in v1, not as a later feature — it’s the #1 reason serious breeders choose BirdTracks", "bullets2"),
        bulletItem("Build spreadsheet import from Day 1 — without it, onboarding breeders with 50+ birds is a non-starter", "bullets2"),
        bulletItem("Implement breeding calendar early — breeders live and die by their calendar; it drives daily engagement", "bullets2"),
        bulletItem("Add QR codes for cage labels — the physical-to-digital bridge is high-value, low-effort", "bullets2"),
        bulletItem("Gamify onboarding with milestone-based trial extensions — BirdTracks proved this works", "bullets2"),
        bulletItem("Give basic analytics (bird count, sex ratio, hatch rate) to free users — don’t paywall what should drive retention", "bullets2"),

        spacer(),
        h2("What I Would Eliminate"),
        bulletItem("Don’t build a full Stats page behind a paywall with no preview — show a blurred preview that drives upgrades", "bullets3"),
        bulletItem("Don’t use purple gradients or dated design patterns — keep the clean neutral palette", "bullets3"),
        bulletItem("Don’t build table-only views — always offer gallery alternative for visual breeders", "bullets3"),
        bulletItem("Don’t use \"---\" dashes for empty data — every empty state is a missed CTA opportunity", "bullets3"),
        bulletItem("Don’t force desktop-first layouts — Bangladesh breeders are mobile-first", "bullets3"),
        bulletItem("Don’t build cage scanning that requires an external QR app — make it native", "bullets3"),

        spacer(),
        h2("The 80/20 Verdict"),
        p("80% of KinBird’s competitive advantage comes from 20% of decisions:"),
        spacer(),
        new Paragraph({ spacing: { after: 80 }, numbering: { reference: "numbers", level: 0 },
          children: [new TextRun({ text: "Ship the mutation predictor ", size: 20, font: "Arial", color: GRAY, bold: true }),
                     new TextRun({ text: "— it’s the single feature that makes serious breeders choose a platform", size: 20, font: "Arial", color: GRAY })] }),
        new Paragraph({ spacing: { after: 80 }, numbering: { reference: "numbers", level: 0 },
          children: [new TextRun({ text: "Build spreadsheet import ", size: 20, font: "Arial", color: GRAY, bold: true }),
                     new TextRun({ text: "— it removes the #1 onboarding friction for established breeders", size: 20, font: "Arial", color: GRAY })] }),
        new Paragraph({ spacing: { after: 80 }, numbering: { reference: "numbers", level: 0 },
          children: [new TextRun({ text: "Keep the UX advantage ", size: 20, font: "Arial", color: GRAY, bold: true }),
                     new TextRun({ text: "— BirdTracks can add features, but they can’t easily redesign their entire UX", size: 20, font: "Arial", color: GRAY })] }),
        new Paragraph({ spacing: { after: 80 }, numbering: { reference: "numbers", level: 0 },
          children: [new TextRun({ text: "Own the Bangladesh market ", size: 20, font: "Arial", color: GRAY, bold: true }),
                     new TextRun({ text: "— Bangla language + BDT pricing + SSLCommerz + local breeder relationships = defensible moat", size: 20, font: "Arial", color: GRAY })] }),

        spacer(), spacer(),
        new Paragraph({ alignment: AlignmentType.CENTER, border: { top: { style: BorderStyle.SINGLE, size: 2, color: GREEN } }, spacing: { before: 200 }, children: [] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80, before: 200 },
          children: [new TextRun({ text: "End of Report", size: 20, font: "Arial", color: GREEN, bold: true, italics: true })] }),
        new Paragraph({ alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "KinBird Pro — Learn from everything. Copy nothing. Build something better.", size: 18, font: "Arial", color: GRAY, italics: true })] }),
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/sessions/pensive-affectionate-einstein/mnt/Projects/Birds Track/BirdTracks-Competitive-Research-Report.docx", buffer);
  console.log("Report generated successfully");
});
