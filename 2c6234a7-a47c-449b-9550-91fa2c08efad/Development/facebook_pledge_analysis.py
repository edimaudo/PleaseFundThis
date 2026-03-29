####################
### Social media Availability
####################
df_view['fb_label'] = df_view['project_has_facebook_page'].apply(lambda x: 'Has Facebook' if x is True else 'No Facebook')
success_df_fb = df_view[df_view['project_success'] == True]
failed_df_fb = df_view[df_view['project_success'] == False]

fig_fb = go.Figure()

fig_fb.add_trace(go.Box(
    x=success_df_fb['fb_label'],
    y=success_df_fb['amt_pledged_$'],
    name='Successful',
    marker_color='#00CC96',
    boxpoints=None
))

fig_fb.add_trace(go.Box(
    x=failed_df_fb['fb_label'],
    y=failed_df_fb['amt_pledged_$'],
    name='Unsuccessful',
    marker_color='#EF553B',
    boxpoints=None
))

fig_fb.update_layout(
    title={'text': 'Social Lift: Impact of Facebook Pages', 'x': 0.5},
    yaxis_title="Total Amount Pledged ($)",
    xaxis_title="Facebook Page Presence",
    boxmode='group',
    template='plotly_white'
)

fig_fb.show()