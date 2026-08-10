def apply_chart_theme(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",

        font=dict(
            family="Segoe UI",
            size=14,
            color="white"
        ),

        title=dict(
            font=dict(
                size=22,
                color="white"
            ),
            x=0.02
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(size=12)
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        hoverlabel=dict(
            bgcolor="#1F2937",
            font_size=14,
            font_family="Segoe UI"
        )

    )

    fig.update_xaxes(

        showgrid=True,
        gridcolor="#2D3748",
        zeroline=False

    )

    fig.update_yaxes(

        showgrid=True,
        gridcolor="#2D3748",
        zeroline=False

    )

    return fig