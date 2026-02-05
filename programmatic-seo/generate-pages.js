#!/usr/bin/env node
/**
 * Programmatic SEO Page Generator for AI Excuse Generator
 * 
 * Generates thousands of SEO-optimized landing pages based on dimension combinations.
 * Run this during build: npm run generate-seo
 */

const fs = require('fs');
const path = require('path');

const dimensions = require('./dimensions.json');

const TOOL_URL = 'https://excuse.demo.densematrix.ai';
const OUTPUT_DIR = path.join(__dirname, '..', 'frontend', 'public', 'p');
const SITEMAP_PATH = path.join(__dirname, '..', 'frontend', 'public', 'sitemap-programmatic.xml');
const SITEMAP_MAIN_PATH = path.join(__dirname, '..', 'frontend', 'public', 'sitemap-main.xml');
const SITEMAP_INDEX_PATH = path.join(__dirname, '..', 'frontend', 'public', 'sitemap.xml');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Generate all combinations
function generateCombinations() {
  const pages = [];
  
  // Combination 1: scenario × recipient × style
  for (const scenario of dimensions.scenarios) {
    for (const recipient of dimensions.recipients) {
      for (const style of dimensions.styles) {
        const slug = `${scenario.id}-${recipient.id}-${style.id}`;
        pages.push({
          slug,
          scenario,
          recipient,
          style,
          industry: null,
          url: `${TOOL_URL}/p/${slug}/`
        });
      }
    }
  }
  
  // Combination 2: scenario × industry × style
  for (const scenario of dimensions.scenarios) {
    for (const industry of dimensions.industries) {
      for (const style of dimensions.styles) {
        const slug = `${scenario.id}-${industry.id}-${style.id}`;
        // Avoid duplicates
        if (!pages.find(p => p.slug === slug)) {
          pages.push({
            slug,
            scenario,
            recipient: null,
            style,
            industry,
            url: `${TOOL_URL}/p/${slug}/`
          });
        }
      }
    }
  }
  
  return pages;
}

// Generate HTML for a single page
function generatePageHTML(page) {
  const { scenario, recipient, style, industry } = page;
  
  const title = recipient 
    ? `${style.name_en} Excuse for ${scenario.name_en} to Your ${recipient.name_en} | AI Excuse Generator`
    : `${style.name_en} ${scenario.name_en} Excuse for ${industry.name_en} | AI Excuse Generator`;
  
  const description = recipient
    ? `Need a ${style.name_en.toLowerCase()} excuse for ${scenario.name_en.toLowerCase()}? Our AI generates perfect excuses for telling your ${recipient.name_en.toLowerCase()}. Try free!`
    : `Generate ${style.name_en.toLowerCase()} excuses for ${scenario.name_en.toLowerCase()} in the ${industry.name_en.toLowerCase()}. AI-powered excuse generator. Try free!`;
  
  const h1 = recipient
    ? `${style.name_en} Excuses for ${scenario.name_en} (${recipient.name_en})`
    : `${style.name_en} ${scenario.name_en} Excuses for ${industry.name_en}`;
  
  const context = recipient ? recipient.name_en : industry.name_en;
  const keywords = scenario.keywords.join(', ');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <meta name="description" content="${description}">
  <meta name="keywords" content="${keywords}, ${style.name_en.toLowerCase()} excuse, ${context.toLowerCase()} excuse">
  <link rel="canonical" href="${page.url}">
  
  <!-- Open Graph -->
  <meta property="og:title" content="${title}">
  <meta property="og:description" content="${description}">
  <meta property="og:url" content="${page.url}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="${TOOL_URL}/og-image.png">
  <meta property="og:site_name" content="AI Excuse Generator">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${title}">
  <meta name="twitter:description" content="${description}">
  
  <!-- JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "AI Excuse Generator - ${h1}",
    "description": "${description}",
    "url": "${page.url}",
    "applicationCategory": "UtilityApplication",
    "operatingSystem": "Web",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    },
    "author": {
      "@type": "Organization",
      "name": "DenseMatrix",
      "url": "https://densematrix.ai"
    }
  }
  </script>
  
  <!-- GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-P4ZLGKH1E1"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-P4ZLGKH1E1', {
      'custom_map': {'dimension1': 'tool_name'}
    });
    gtag('event', 'page_view', {
      'tool_name': 'excuse-generator',
      'page_type': 'programmatic_seo'
    });
  </script>
  
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Courier New', monospace; background: #faf8f5; color: #2d2d2d; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }
    h1 { font-size: 1.8rem; margin-bottom: 1rem; color: #1a1a1a; }
    h2 { font-size: 1.3rem; margin: 1.5rem 0 0.5rem; color: #333; }
    p { margin-bottom: 1rem; }
    .cta { background: #e74c3c; color: white; padding: 15px 30px; text-decoration: none; display: inline-block; margin: 20px 0; border-radius: 5px; font-weight: bold; }
    .cta:hover { background: #c0392b; }
    .related { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ddd; }
    .related a { display: inline-block; margin: 5px 10px 5px 0; color: #e74c3c; }
    footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ddd; font-size: 0.9rem; color: #666; }
  </style>
</head>
<body>
  <h1>${h1}</h1>
  
  <p>Looking for the perfect <strong>${style.name_en.toLowerCase()}</strong> excuse for <strong>${scenario.name_en.toLowerCase()}</strong>? 
  Our AI-powered excuse generator creates ${recipient ? `customized excuses for telling your ${recipient.name_en.toLowerCase()}` : `industry-specific excuses perfect for ${industry.name_en.toLowerCase()} professionals`}.</p>
  
  <h2>Why Use Our ${style.name_en} Excuse Generator?</h2>
  <p>Sometimes life happens and you need a good excuse. Whether it's ${scenario.keywords.slice(0, 3).join(', ')}, 
  our AI understands the nuances of ${recipient ? `communicating with your ${recipient.name_en.toLowerCase()}` : `the ${industry.name_en.toLowerCase()}`} 
  and generates ${style.name_en.toLowerCase()} excuses that actually work.</p>
  
  <h2>How It Works</h2>
  <p>1. Select your situation (${scenario.name_en})<br>
  2. Choose your tone (${style.name_en})<br>
  3. Get an AI-generated excuse instantly<br>
  4. Copy and use!</p>
  
  <a href="${TOOL_URL}?scenario=${scenario.id}&style=${style.id}${recipient ? '&recipient=' + recipient.id : ''}${industry ? '&industry=' + industry.id : ''}" class="cta">
    Generate Your ${style.name_en} Excuse Now →
  </a>
  
  <div class="related">
    <h2>Related Excuses</h2>
    ${generateRelatedLinks(page)}
  </div>
  
  <footer>
    <p>© 2024 <a href="https://densematrix.ai">DenseMatrix</a> | <a href="${TOOL_URL}">AI Excuse Generator</a></p>
  </footer>
</body>
</html>`;
}

// Generate related links for internal linking
function generateRelatedLinks(currentPage) {
  const related = [];
  const { scenario, recipient, style, industry } = currentPage;
  
  // Same scenario, different style
  const otherStyles = dimensions.styles.filter(s => s.id !== style.id).slice(0, 2);
  for (const s of otherStyles) {
    const slug = recipient 
      ? `${scenario.id}-${recipient.id}-${s.id}`
      : `${scenario.id}-${industry.id}-${s.id}`;
    related.push({ slug, label: `${s.name_en} ${scenario.name_en} Excuse` });
  }
  
  // Same style, different scenario
  const otherScenarios = dimensions.scenarios.filter(sc => sc.id !== scenario.id).slice(0, 2);
  for (const sc of otherScenarios) {
    const slug = recipient
      ? `${sc.id}-${recipient.id}-${style.id}`
      : `${sc.id}-${industry ? industry.id : dimensions.industries[0].id}-${style.id}`;
    related.push({ slug, label: `${style.name_en} ${sc.name_en} Excuse` });
  }
  
  return related.map(r => `<a href="${TOOL_URL}/p/${r.slug}/">${r.label}</a>`).join('\n    ');
}

// Generate sitemap XML
function generateSitemaps(pages) {
  const today = new Date().toISOString().split('T')[0];
  
  // Sitemap for programmatic pages
  let programmaticXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
`;
  
  for (const page of pages) {
    programmaticXml += `  <url>
    <loc>${page.url}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
`;
  }
  
  programmaticXml += '</urlset>';
  fs.writeFileSync(SITEMAP_PATH, programmaticXml);
  
  // Main sitemap
  const mainXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${TOOL_URL}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>`;
  fs.writeFileSync(SITEMAP_MAIN_PATH, mainXml);
  
  // Sitemap index
  const indexXml = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>${TOOL_URL}/sitemap-main.xml</loc></sitemap>
  <sitemap><loc>${TOOL_URL}/sitemap-programmatic.xml</loc></sitemap>
</sitemapindex>`;
  fs.writeFileSync(SITEMAP_INDEX_PATH, indexXml);
}

// Main
function main() {
  console.log('🚀 Generating programmatic SEO pages...');
  
  const pages = generateCombinations();
  console.log(`📊 Total pages to generate: ${pages.length}`);
  
  let generated = 0;
  for (const page of pages) {
    const pageDir = path.join(OUTPUT_DIR, page.slug);
    if (!fs.existsSync(pageDir)) {
      fs.mkdirSync(pageDir, { recursive: true });
    }
    
    const html = generatePageHTML(page);
    fs.writeFileSync(path.join(pageDir, 'index.html'), html);
    generated++;
    
    if (generated % 1000 === 0) {
      console.log(`  Generated ${generated}/${pages.length} pages...`);
    }
  }
  
  console.log('📁 Generating sitemaps...');
  generateSitemaps(pages);
  
  console.log(`✅ Done! Generated ${generated} pages + sitemaps`);
}

main();
