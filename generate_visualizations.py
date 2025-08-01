#!/usr/bin/env python3
"""
AI Conversation in Kenya - Visualization Generator
Generates engaging visualizations from AI conversation data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import os
from collections import Counter

# Set style
plt.style.use('default')
sns.set_palette('husl')

# Create visuals directory if it doesn't exist
os.makedirs('visuals', exist_ok=True)

# Twitter conversation data from scraped content
twitter_data = {
    'tweet_text': [
        'The artificial intelligence industry is scrambling to reduce its massive energy consumption through better cooling systems',
        'Startups in artificial intelligence and fintech are struggling to process growing volumes of sensitive data',
        'Recently, tech giant Microsoft announced the largest round of layoffs since 2023',
        'A rising tide of artificial intelligence (AI) bands is ushering in a new era where work will be scarcer for musicians',
        'Tanzanian entrepreneur Yvonne Baldwin has made history by winning two prestigious awards at the AI for Good Innovation Factory 2025',
        'Young Scientists Kenya (YSK) has trained 170 secondary school teachers in Artificial Intelligence',
        'MTN Group has embarked on an exciting journey to leverage responsible Artificial Intelligence',
        'Ecobank Group has announced a strategic partnership with Google Cloud to accelerate financial inclusion',
        'Kenya has emerged as the world\'s number one user of ChatGPT',
        'Meta Platforms Inc. has acquired PlayAI, a Cairo-founded artificial intelligence startup'
    ],
    'sentiment': ['negative', 'negative', 'negative', 'negative', 'positive', 'positive', 'positive', 'positive', 'positive', 'positive'],
    'category': [
        'Environmental Impact', 'Data Processing', 'Workforce Impact', 'Creative Industry',
        'Innovation Awards', 'Education', 'Infrastructure', 'Financial Services',
        'Technology Adoption', 'Acquisitions'
    ],
    'engagement_score': [85, 72, 95, 88, 92, 78, 65, 70, 100, 90]
}

twitter_df = pd.DataFrame(twitter_data)

print('🚀 Starting AI Conversation Analysis...')
print(f'📊 Dataset contains {len(twitter_df)} AI conversation posts')

# 1. Sentiment Analysis Visualization
print('\n📈 Creating sentiment analysis visualization...')
sentiment_counts = twitter_df['sentiment'].value_counts()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Pie chart
colors = ['#ff6b6b', '#4ecdc4']
ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90)
ax1.set_title('AI Conversation Sentiment Distribution', fontsize=14, fontweight='bold')

# Bar chart
bars = ax2.bar(sentiment_counts.index, sentiment_counts.values, color=colors)
ax2.set_title('Sentiment Count', fontsize=14, fontweight='bold')
ax2.set_ylabel('Number of Posts')
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('visuals/sentiment_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Category Analysis with Engagement
print('📊 Creating category engagement analysis...')
fig, ax = plt.subplots(figsize=(12, 8))

# Create scatter plot
colors = ['red' if s == 'negative' else 'green' for s in twitter_df['sentiment']]
scatter = ax.scatter(twitter_df['category'], twitter_df['engagement_score'], 
                    c=colors, s=100, alpha=0.7)

ax.set_xlabel('Conversation Category', fontweight='bold')
ax.set_ylabel('Engagement Score', fontweight='bold')
ax.set_title('AI Conversation Categories vs Engagement Levels', fontsize=16, fontweight='bold')
plt.xticks(rotation=45, ha='right')

# Add legend
red_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Negative')
green_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='Positive')
ax.legend(handles=[red_patch, green_patch])

plt.tight_layout()
plt.savefig('visuals/category_engagement.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Word Cloud Generation
print('☁️ Creating word cloud...')
all_text = ' '.join(twitter_df['tweet_text'])
# Clean text for word cloud
all_text = re.sub(r'[^\w\s]', '', all_text.lower())
wordcloud = WordCloud(width=800, height=400, background_color='white', 
                     colormap='viridis', max_words=100).generate(all_text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Key Terms in AI Conversations', fontsize=16, fontweight='bold', pad=20)
plt.savefig('visuals/wordcloud.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Top Keywords Analysis
print('🔍 Analyzing top keywords...')
# Extract important words
stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'has', 'have', 'had'}
words = re.findall(r'\b\w+\b', all_text.lower())
filtered_words = [word for word in words if len(word) > 3 and word not in stop_words]
word_counts = Counter(filtered_words)
top_words = dict(word_counts.most_common(10))

plt.figure(figsize=(12, 6))
bars = plt.bar(top_words.keys(), top_words.values(), color='skyblue')
plt.title('Most Frequently Mentioned Terms', fontsize=16, fontweight='bold')
plt.xlabel('Terms')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('visuals/top_keywords.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Interactive Plotly Dashboard Data Preparation
print('🎯 Creating interactive visualizations...')

# Treemap for categories
fig_treemap = px.treemap(
    twitter_df, 
    path=['sentiment', 'category'], 
    values='engagement_score',
    title='AI Conversation Topics by Sentiment & Engagement',
    color='engagement_score',
    color_continuous_scale='RdYlGn'
)
fig_treemap.write_html('visuals/treemap_interactive.html')

# Engagement trend
fig_trend = px.bar(
    twitter_df, 
    x='category', 
    y='engagement_score',
    color='sentiment',
    title='Engagement Scores by Category and Sentiment',
    color_discrete_map={'positive': '#2ecc71', 'negative': '#e74c3c'}
)
fig_trend.update_layout(xaxis_tickangle=-45)
fig_trend.write_html('visuals/engagement_trend.html')

# 6. Generate Summary Statistics
print('📋 Generating summary insights...')

insights = {
    'total_posts': int(len(twitter_df)),
    'positive_ratio': float((twitter_df['sentiment'] == 'positive').mean() * 100),
    'avg_engagement': float(twitter_df['engagement_score'].mean()),
    'top_category': str(twitter_df.loc[twitter_df['engagement_score'].idxmax(), 'category']),
    'highest_engagement': int(twitter_df['engagement_score'].max()),
    'sentiment_distribution': {k: int(v) for k, v in twitter_df['sentiment'].value_counts().to_dict().items()},
    'category_counts': {k: int(v) for k, v in twitter_df['category'].value_counts().to_dict().items()}
}

# Save insights to JSON for dashboard
import json
with open('visuals/insights.json', 'w') as f:
    json.dump(insights, f, indent=2)

print('\n✅ Visualization generation complete!')
print(f'📁 All files saved to visuals/ directory')
print(f'📊 Key Insights:')
print(f'   • {insights["positive_ratio"]:.1f}% of conversations are positive')
print(f'   • Average engagement score: {insights["avg_engagement"]:.1f}')
print(f'   • Highest performing category: {insights["top_category"]} ({insights["highest_engagement"]} engagement)')
print(f'   • Most discussed categories: {", ".join(list(insights["category_counts"].keys())[:3])}')

# Display file listing
print(f'\n📋 Generated files:')
for file in os.listdir('visuals'):
    print(f'   • {file}')