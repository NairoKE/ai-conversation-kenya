# AI Conversation in Kenya - Deployment Guide

## 🚀 Live Dashboard

The interactive dashboard showcases AI conversation insights from Kenya, featuring:

- **Sentiment Analysis**: 60% positive sentiment toward AI adoption
- **Engagement Metrics**: Technology adoption leads with 100 engagement score  
- **Key Findings**: Kenya ranks #1 globally in ChatGPT usage (42.1%)
- **Interactive Visualizations**: Treemap and trend analysis
- **Word Clouds**: Most discussed terms in AI conversations

## 📊 Dashboard Features

### Static Visualizations
- Sentiment distribution pie chart and bar chart
- Category engagement scatter plot with sentiment coloring
- Word cloud of key terms in AI conversations
- Top 10 most frequently mentioned keywords

### Interactive Components
- Treemap showing topic hierarchy by engagement and sentiment
- Bar chart comparing engagement across categories
- Real-time data loading from insights.json

### Key Statistics Panel
- Total conversations analyzed: 10
- Positive sentiment ratio: 60%
- Average engagement score: 83.5
- Highest engagement category: Technology Adoption (100)

## 🌐 Deployment Options

### Option 1: GitHub Pages (Recommended)
1. Push repository to GitHub
2. Go to repository Settings > Pages
3. Select source: Deploy from branch (main)
4. Your dashboard will be live at: `https://yourusername.github.io/ai-conversation-kenya`

### Option 2: Netlify
1. Connect your GitHub repository to Netlify
2. Set build command: (leave empty - static site)
3. Set publish directory: `/` (root)
4. Deploy automatically on git push

### Option 3: Vercel
1. Import project from GitHub to Vercel
2. No build configuration needed
3. Automatic deployments on commits

### Option 4: Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/ai-conversation-kenya
cd ai-conversation-kenya

# Open with live server (VS Code extension) or
python -m http.server 8000
# Then visit http://localhost:8000
```

## 📁 File Structure for Deployment

```
├── index.html              # Main dashboard page
├── generate_visualizations.py  # Data processing script
├── visuals/                # Generated charts and data
│   ├── *.png              # Static visualizations
│   ├── *.html             # Interactive Plotly charts
│   └── insights.json      # Key metrics data
├── data/                  # Data collection templates
├── notebook/              # Jupyter analysis notebooks
└── requirements.txt       # Python dependencies
```

## 🔧 Customization

### Updating Data
1. Run `python generate_visualizations.py` with new data
2. New visualizations will be generated in `visuals/` folder
3. Dashboard automatically loads updated insights.json

### Styling
- Edit CSS in `index.html` `<style>` section
- Modify color schemes, fonts, and layout
- All styling is contained in the single HTML file

### Adding New Visualizations
1. Generate new charts in `generate_visualizations.py`
2. Save as PNG (static) or HTML (interactive)
3. Add new chart cards to dashboard HTML

## 📱 Mobile Responsive

The dashboard is fully responsive with:
- Flexible grid layouts
- Mobile-optimized font sizes
- Touch-friendly interactive elements
- Smooth animations and transitions

## 🔗 Social Sharing

Pre-configured sharing buttons for:
- LinkedIn post about insights
- GitHub repository link
- Full report download (placeholder)

## 📈 Performance

- Lightweight HTML/CSS/JS (no heavy frameworks)
- Optimized images (PNG compression)
- Fast loading interactive charts (Plotly)
- Minimal external dependencies

## 🛠️ Future Enhancements

- Real-time data updates via API
- More sophisticated sentiment analysis
- Geographic mapping of conversations
- Historical trend analysis
- User filtering and search capabilities

---

**Ready to deploy?** Choose your preferred option above and share your AI insights with the world! 🌍