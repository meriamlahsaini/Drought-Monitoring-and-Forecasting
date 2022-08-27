import streamlit as st


def app():
    st.title("Introduction")
    
    st.sidebar.title("About")
    st.sidebar.info(
    """
    Web App URL: <https://rim-chan-dm-app-344y39.streamlitapp.com/>
    GitHub repository: <https://github.com/Rim-chan/DM>
    """
    )

    st.sidebar.title("Contact")
    st.sidebar.info(
        """
        [GitHub](https://github.com/Rim-chan) |[LinkedIn](https://www.linkedin.com/in/rim-sleimi/)
        """
    )
    

    st.info('This multi-page web app demonstrates drought monitoring an forecasting created using [streamlit](https://streamlit.io) and open-source mapping libraries, such as [leafmap](https://leafmap.org), [geemap](https://geemap.org), [pydeck](https://deckgl.readthedocs.io), and [kepler.gl](https://docs.kepler.gl/docs/keplergl-jupyter).)
   
    st.markdown(
        """
    Drought is a climate-related disaster that negatively impacts a variety of sectors and poses challenges for millions of people especially in African countries.
    The occurrence and the increase in drought severity result in significant losses to the farming community. As an agrarian economy, establishing drought monitoring
    and early warning systems can help decision-makers better act in response to drought. The overarching objective
    of this study is to address this problem through the development of a drought monitoring and forecasting system, leveraging the synergistic use of
    Principal Component Analysis (PCA) and convolutional long short term memory (ConvLSTM) over the countries of interest.

    """
    )
