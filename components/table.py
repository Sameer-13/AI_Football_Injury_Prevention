import streamlit as st
import pandas as pd

def display_player_table(player_df):
    """
    Display a modern styled table of players with injury predictions
    
    Args:
        player_df: DataFrame containing player data with risk assessments
        
    Returns:
        DataFrame: Processed player display DataFrame
    """
    # Color function for styling
    def color_injury_prediction(val):
        if val == 'High Risk':
            return 'background-color: rgba(231, 76, 60, 0.9); color: white; font-weight: bold; border-radius: 5px; padding: 0.3rem 0.6rem; text-align: center;'
        else:
            return 'background-color: rgba(93, 184, 92, 0.9); color: white; font-weight: bold; border-radius: 5px; padding: 0.3rem 0.6rem; text-align: center;'
    
    # Add custom styling to position column
    def style_position(val):
        position_colors = {
            "Goalkeeper": "background-color: rgba(241, 196, 15, 0.2); border-left: 3px solid #F1C40F;",
            "Defender": "background-color: rgba(52, 152, 219, 0.2); border-left: 3px solid #3498DB;",
            "Midfielder": "background-color: rgba(155, 89, 182, 0.2); border-left: 3px solid #9B59B6;",
            "Forward": "background-color: rgba(231, 76, 60, 0.2); border-left: 3px solid #E74C3C;",
        }
        return position_colors.get(val, "")
    
    # Style the rating column 
    def style_rating(val):
        try:
            rating = float(val)
            if rating >= 7.0:
                return "color: #5DB85C; font-weight: bold;"
            elif rating >= 6.0:
                return "color: #F1C40F; font-weight: bold;"
            else:
                return "color: #E74C3C; font-weight: bold;"
        except:
            return ""
    
    # Create a copy of the dataframe for display
    display_df = player_df.copy()
    
    # Ensure numeric columns are formatted properly
    if 'Age' in display_df.columns:
        display_df['Age'] = display_df['Age'].apply(lambda x: f"{float(x):.0f}" if pd.notnull(x) else "N/A")
    
    if 'Rating' in display_df.columns:
        display_df['Rating'] = display_df['Rating'].apply(lambda x: f"{float(x):.2f}" if pd.notnull(x) else "N/A")
    
    if 'Height (cm)' in display_df.columns:
        display_df['Height (cm)'] = display_df['Height (cm)'].apply(lambda x: f"{float(x):.0f}" if pd.notnull(x) else "N/A")
    
    if 'Weight (kg)' in display_df.columns:
        display_df['Weight (kg)'] = display_df['Weight (kg)'].apply(lambda x: f"{float(x):.0f}" if pd.notnull(x) else "N/A")
    
    if 'Minutes Played' in display_df.columns:
        display_df['Minutes Played'] = display_df['Minutes Played'].apply(lambda x: f"{float(x):.0f}" if pd.notnull(x) else "N/A")
    
    # Style and display the DataFrame
    styled_df = (
        display_df.drop(columns=['Injury Prediction'])
        .style
        .applymap(color_injury_prediction, subset=["Injury Risk"])
        .applymap(style_position, subset=["Position"])
        .applymap(style_rating, subset=["Rating"])
        .set_properties(**{
            'text-align': 'center',
            'font-size': '14px',
            'border': 'none',
            'background-color': '#2C2F44',
            'color': 'white'
        })
        .set_table_styles([
            {'selector': 'th', 'props': [
                ('background-color', '#1E2130'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('text-align', 'center'),
                ('border', 'none'),
                ('padding', '10px'),
                ('font-size', '14px')
            ]},
            {'selector': 'tr:hover', 'props': [
                ('background-color', '#3b3f5c')
            ]},
            {'selector': 'td', 'props': [
                ('padding', '10px')
            ]}
        ])
    )
    
    # Display the styled table
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add table legends/info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div style="background-color: #2C2F44; border-radius: 10px; padding: 1rem; text-align: center;">
                <span style="background-color: rgba(231, 76, 60, 0.9); color: white; font-weight: bold; border-radius: 5px; padding: 0.3rem 0.6rem;">High Risk</span>
                <span style="margin-left: 0.5rem; color: #b0b0b0;">Players requiring special attention</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style="background-color: #2C2F44; border-radius: 10px; padding: 1rem; text-align: center;">
                <span style="background-color: rgba(93, 184, 92, 0.9); color: white; font-weight: bold; border-radius: 5px; padding: 0.3rem 0.6rem;">Low Risk</span>
                <span style="margin-left: 0.5rem; color: #b0b0b0;">Players with normal injury risk</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        # Add filter/search options
        st.markdown(
            """
            <div style="background-color: #2C2F44; border-radius: 10px; padding: 1rem; text-align: center;">
                <button style="background-color: #5762D5; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer; font-weight: 600;">
                    <span style="margin-right: 0.5rem;">📊</span> Export Data
                </button>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return player_df