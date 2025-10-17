# 🛒 Lulu Hypermart Business Analytics Dashboard

A comprehensive business analytics dashboard for Lulu Hypermart UAE, providing actionable insights for strategic decision-making.

## 📋 Features

- **Monthly Sales Trend Analysis** - Track sales performance over time
- **Online vs Offline Sales Comparison** - Channel performance metrics
- **Day of Week Analysis** - Optimize staffing and promotions
- **Geographic Sales Analysis** - City and zone-based product localization
- **Average Order Value (AOV) Analysis** - Customer segmentation and retention strategies
- **Interactive Filters** - Filter by Department, Category, Nationality, and Age
- **Detailed Insights** - Textual recommendations and tabular data views

## 🚀 Deployment on Streamlit Cloud

### Step 1: Prepare Your Files

Create a folder structure like this:
```
lulu-analytics-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── lulu_uae_master_2000.csv  # Your dataset goes here
└── .gitignore (optional)
```

### Step 2: Upload to GitHub

1. Create a new repository on GitHub (e.g., `lulu-analytics-dashboard`)
2. Initialize git in your local folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Lulu Analytics Dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/lulu-analytics-dashboard.git
   git push -u origin main
   ```

### Step 3: Deploy on Streamlit Cloud

1. Go to [streamlit.io](https://streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `lulu-analytics-dashboard`
5. Set main file path: `app.py`
6. Click "Deploy"

Your dashboard will be live in a few minutes! 🎉

## 📊 Dataset Requirements

Your `lulu_uae_master_2000.csv` should contain the following columns (adjust column names in app.py if different):

- **Date column** - Transaction date
- **Sales/Amount/Revenue column** - Transaction value
- **Department** - Product department
- **Category** - Product category
- **Nationality** - Customer nationality
- **Age** - Customer age
- **City** - Transaction city
- **City_zone** - City zone/area
- **Channel/Type** - Online or Offline
- **Product** - Product name

## 🔧 Local Development

To run the dashboard locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📝 Customization

### Updating Column Names

If your dataset has different column names, update these sections in `app.py`:

```python
# Lines 45-50: Update column name references
date_columns = [col for col in df.columns if 'date' in col.lower()]
sales_col = [col for col in df.columns if 'sales' in col.lower()]
```

### Adding New Visualizations

Add new charts in the main() function using Plotly:

```python
fig = px.bar(data, x='column1', y='column2', title='My Chart')
st.plotly_chart(fig, use_container_width=True)
```

## 🎯 Business Insights Provided

1. **Sales Trends** - Identify peak and low-performing months
2. **Channel Performance** - Compare online vs offline sales
3. **Operational Efficiency** - Optimize staffing based on busy days
4. **Product Localization** - Tailor inventory to local preferences
5. **Customer Retention** - Segment customers and design loyalty programs

## 🔐 Security Notes

- Do not commit sensitive data to public repositories
- Use `.gitignore` to exclude data files if needed
- Consider using Streamlit secrets for API keys or credentials

## 📄 .gitignore (Optional)

Create a `.gitignore` file to exclude unnecessary files:

```
*.csv
*.xlsx
__pycache__/
*.pyc
.DS_Store
.env
```

## 💡 Tips for Success

- Ensure your CSV file is clean and properly formatted
- Test locally before deploying to Streamlit Cloud
- Monitor your Streamlit Cloud logs for any errors
- Update requirements.txt if you add new libraries

## 📞 Support

For issues or questions:
- Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- GitHub Issues: Create an issue in your repository
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)

## 📜 License

This project is open-source and available for business use.

---

**Created for Lulu Hypermart UAE** | Business Analytics Dashboard | 2025