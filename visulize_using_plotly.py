import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots as sp

data = pd.read_csv('noon_products.csv')
data.columns = [
    "Date & Time", "SKU", "Title", "Brand", "Average Rating", "Rating Count", 
    "Sponsored", "Price", "Old Price", "Discount", "Express", "Rank", "Link"
]


def clean_price(price):
    try:
     
        cleaned = price.replace('AED', '').replace(',', '').strip()
        return float(cleaned)
    except:
        return None


data['Price'] = data['Price'].apply(clean_price)
data = data.dropna(subset=['Price'])
data_sorted_expensive = data.sort_values(by='Price', ascending=False).head(20)
data_sorted_cheap = data.sort_values(by='Price', ascending=True).head(20)


color_palette = px.colors.qualitative.Plotly

fig = go.Figure()


fig.add_trace(
    go.Bar(
        x=data_sorted_expensive['Title'],
        y=data_sorted_expensive['Price'],
        name='Most Expensive Products',
        text=[f'AED {price:.2f}' for price in data_sorted_expensive['Price']],
        textposition='outside',
        marker_color=[color_palette[i % len(color_palette)] for i in range(len(data_sorted_expensive))],
        hovertext=[f'Product: {title}<br>Brand: {brand}<br>Price: AED {price:.2f}' 
                   for title, brand, price in zip(data_sorted_expensive['Title'], 
                                                  data_sorted_expensive['Brand'], 
                                                  data_sorted_expensive['Price'])]
    )
)


fig.add_trace(
    go.Bar(
        x=data_sorted_cheap['Title'],
        y=data_sorted_cheap['Price'],
        name='Cheapest Products',
        text=[f'AED {price:.2f}' for price in data_sorted_cheap['Price']],
        textposition='outside',
        marker_color=[color_palette[i % len(color_palette)] for i in range(len(data_sorted_cheap))],
        hovertext=[f'Product: {title}<br>Brand: {brand}<br>Price: AED {price:.2f}' 
                   for title, brand, price in zip(data_sorted_cheap['Title'], 
                                                  data_sorted_cheap['Brand'], 
                                                  data_sorted_cheap['Price'])]
    )
)

brand_counts = data['Brand'].value_counts()
fig.add_trace(
    go.Bar(
        x=brand_counts.index,
        y=brand_counts.values,
        name='Products by Brand',
        text=brand_counts.values,
        textposition='outside',
        marker_color=[color_palette[i % len(color_palette)] for i in range(len(brand_counts))]
    )
)


seller_counts = data['Brand'].value_counts()  
fig.add_trace(
    go.Bar(
        x=seller_counts.index,
        y=seller_counts.values,
        name='Products by Seller',
        text=seller_counts.values,
        textposition='outside',
        marker_color=[color_palette[i % len(color_palette)] for i in range(len(seller_counts))]
    )
)

dropdown_options = [{'label': 'All Brands', 'value': 'All'}]
dropdown_options.extend([{'label': brand, 'value': brand} for brand in data['Brand'].unique()])

fig.update_layout(
    height=1000,  
    width=1500,
    title='Product Analysis',
    template='plotly_white',
    updatemenus=[
        {
            'buttons': [
                {
                    'method': 'update',
                    'label': option['label'],
                    'args': [
                        {
                            'visible': [
                                option['value'] == 'All' or 
                                (option['value'] in data_sorted_expensive['Brand'].values),
                                option['value'] == 'All' or 
                                (option['value'] in data_sorted_cheap['Brand'].values),
                                option['value'] == 'All',
                                option['value'] == 'All'
                            ]
                        },
                        {'title': f'Product Analysis - {option["label"]}'}
                    ]
                } for option in dropdown_options
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        }
    ]
)


fig.update_xaxes(title_text='Products', tickangle=-45)
fig.update_yaxes(title_text='Price/Count')


fig.update_layout(
    scene = dict(
        xaxis_title='Products',
        yaxis_title='Price/Count'
    ),
    title='Product Analysis',
)

fig.show()