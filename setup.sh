mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"heroku.saucy764@passmail.net\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml