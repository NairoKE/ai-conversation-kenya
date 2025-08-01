# Who's Talking AI in Kenya?

## Project Overview
This project analyzes how organizations and leaders in Kenya are communicating about AI, workforce upskilling, and digital transformation across Twitter and LinkedIn. We focus on identifying key voices, their seniority levels, and the impact of their messages in the digital transformation conversation.

## Research Questions
- Which companies, startups, and public organizations in Kenya are actively discussing AI and digital transformation?
- What language and terminology are they using in these discussions?
- What is the seniority profile of LinkedIn contributors to this conversation?
- How does Twitter account influence correlate with AI discussion engagement?
- What trends emerge in workforce development and digital adoption messaging?

## Data Sources
1. Twitter/X Data:
   - Keywords tracked: "AI Kenya", "digital transformation", "machine learning Kenya", "future-proof workforce", "AI reskilling"
   - Metrics: username, follower count, engagement rates, verified status
   
2. LinkedIn Data:
   - Organization pages and individual posts
   - Poster seniority levels
   - Company size and sector
   - Engagement metrics

## Project Structure
```
ai-in-kenya/
│
├── data/
│   ├── twitter_data.csv
│   └── linkedin_data.csv
├── notebook/
│   ├── data_collection.ipynb
│   └── analysis.ipynb
├── visuals/
│   ├── wordcloud.png
│   ├── top_orgs_chart.png
│   ├── seniority_distribution.png
│   └── engagement_metrics.png
└── README.md
```

## Analysis Approach
1. Data Collection
   - Twitter API scraping using Tweepy
   - Manual LinkedIn data collection with seniority classification
   - Profile metrics gathering and categorization

2. Analysis Components
   - Organization activity levels
   - Content analysis and keyword extraction
   - Seniority level impact analysis
   - Engagement metrics correlation
   - Temporal trend analysis

3. Visualization
   - Word clouds by platform
   - Organization activity charts
   - Seniority distribution plots
   - Engagement correlation matrices

## Setup Instructions
1. Clone this repository
2. Install required packages: `pip install -r requirements.txt`
3. Configure API credentials in `config.py`
4. Run notebooks in sequence

## Dependencies
- Python 3.8+
- Tweepy
- Pandas
- Matplotlib
- Seaborn
- WordCloud
- NLTK

## Results and Insights
[To be updated as analysis progresses]

## Contributing
Feel free to fork this repository and submit pull requests with improvements.

## License
MIT License 