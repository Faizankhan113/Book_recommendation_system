import pandas as pd
from dash import Dash, html, dcc, Output, Input, State


app = Dash(__name__)


def book_rec_sys(my_book):
    df_book= pd.read_csv('Books.csv' , usecols=['ISBN','Book-Title','Book-Author','Year-Of-Publication'],dtype={'Year-Of-Publication':'int16'})
    # to remove duplcate entries based on book-title
    df_book = df_book.drop_duplicates(subset='Book-Title').reset_index(drop=True)
    df_user=pd.read_csv('Ratings.csv' , usecols=['User-ID','ISBN'])

    # making sure the column ISBN always has 10 character if it has less than 10 character then filling the mising character as 0 from left side
    df_book['ISBN'] = df_book['ISBN'].astype(str).str.zfill(10)

    # finding the list of their authors 
    books_author=df_book.loc[df_book['Book-Title'].isin(my_book),'Book-Author'].unique()

    # assigning scores to books
    df_book['score']=0.0
    df_book.loc[df_book['Book-Title'].isin(my_book),'score'] = 1
    df_book.loc[df_book['Book-Author'].isin(books_author),'score'] += 0.25

    # selecting books with score grater that 0
    df_book_score= (
        df_book[df_book['score'] > 0]
        .sort_values(by='score' , ascending=False)
        .copy()
    )

    # merging of df_book_score & df_user for making a df with both ISBN and User-ID
    df_user_score= pd.merge(df_book_score, df_user, how='inner', on='ISBN').sort_values(by='score',ascending=False)

    # obtaning user score
    user_total_score = (
        df_user_score.groupby('User-ID')                        
        .agg(
            total_score=('score', 'sum'),
            rating_count=('score', 'count')
        )
        .sort_values(by=['total_score','rating_count'], ascending=False)
        .reset_index()
    )
    # getting the users which has more than or equal to 2 score
    top_users= user_total_score[user_total_score['total_score']>=2].head(100)

    # merginf dfs for getting df which has User-Id , ISBN and total_score of user
    merged_df= (
        pd.merge(top_users,df_user_score,how='inner',on='User-ID')
        .sort_values(by='total_score',ascending=False)
        .reset_index(drop=True)
        [['User-ID','total_score','ISBN']]
    )

    # for finding final book score
    grouped= (
        merged_df.groupby('ISBN')
        .agg(
            book_score= ('total_score','sum'),
            total_count= ('total_score','count')
        )
        .sort_values(by='book_score',ascending=False)
        .reset_index()
    )

    # merging for getting Book-Title
    final_grouped= pd.merge(grouped,df_book_score,how='inner',on='ISBN')[['ISBN', 'Book-Title', 'book_score','Book-Author']]

    # getting top 5 rated books for suggesting excluding the books already read by the user
    top_5_books=(
        final_grouped[~final_grouped['Book-Title'].isin(my_book)]
        .reset_index(drop=True)
        .head(5)
    )

    return top_5_books



app.layout= html.Div([
        
        # for history section
        html.Div([
            html.Div(
                id='show_history',
                style={
                    'display':'none',
                    'position': 'absolute',
                    'top':'-100px',           
                    'left': '-290px',  
                    'marginRight':'30px',
                    'backgroundColor':'white',
                    "height": "300px",
                    'width':'250px',
                    "overflowY": "auto",
                    "overflowX": "auto",
                    'border':'2px solid black',
                    'paddingRight': '30px',
                }
            ),
            html.Button(
                'Read History',
                id='btn_history',
                n_clicks=0,
                style={'height': '33px','marginRight':'30px',"cursor": "pointer"}
            )],
            style={'position': 'relative','display':'flex',}
        ),

        # for book searching
        dcc.Dropdown(
            id='book_dropdown',
            options=[],
            placeholder='Enter The Book Name',
            searchable=True,
            clearable=True,
            style={'width':'400px','marginRight':'30px',}
        ),
        
        # for Add To Read Books button
        html.Button(
            'Add To Read Books',
            id='btn_submit',
            n_clicks=0,
            style={'height': '33px',"cursor": "pointer"},
        ),
        
        # for reccomendation section
        html.Div([
            html.Button(
                'Recomend books',
                id='btn_rec_book',
                n_clicks=0,
                style={'height': '33px',"cursor": "pointer",'marginLeft':'30px'},
            ),
            html.Div(
                id='show_recomendation',
                style={
                    'display':'none',
                    'position': 'absolute',
                    'top':'-100px',           
                    'left': '165px',  
                    'backgroundColor':'white',
                    "height": "300px",
                    'width':'250px',
                    "overflowY": "auto",
                    'border':'2px solid black',
                    'paddingRight': '30px',
                }
            )],
            style={
                'position': 'relative',
                'display':'flex',
            }
        )],
        
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "height": "100vh"
        }
    )


df_book_name=pd.read_csv('Books.csv' , usecols=['Book-Title'])
@app.callback(
    Output('book_dropdown','options'),
    Input('book_dropdown','search_value'),
    Input('book_dropdown','value'),
    prevent_initial_call= True
)

def update_options(search_value,current_value):

    if current_value and not search_value:
        df_list=df_book_name[df_book_name['Book-Title'].str.contains(current_value[:6],case=False,na=False)]['Book-Title'].unique()[:5]
        option=[{'label':current_value,'value':current_value}]+[{'label':book,'value':book} for book in df_list]
        return option
    
    if search_value :
        df_list=df_book_name[df_book_name['Book-Title'].str.contains(search_value,case=False,na=False)]['Book-Title'].unique()[:5]
        option=[{'label':book,'value':book} for book in df_list]
        return option

    return []
    


readed_books=set()
@app.callback(
    Output('book_dropdown','value'),
    Input('btn_submit','n_clicks'),
    State('book_dropdown','value'),
    prevent_initial_call= True
)

def upadting_readed_books(_,value):
    if value:
        readed_books.add(value)
        print('added',value)
        return ''
    return value



@app.callback(
    Output('show_history','style'),
    Output('show_history','children'),
    Input('btn_history','n_clicks'),
    State('show_history','style'),
    prevent_initial_call=True
)

def showing_history(click,style):
    if click % 2 == 0:
        style['display']='none'

    else:
        style['display']='block'

    text= html.Ul(
        [html.Li(book,style={"marginBottom": "12px"})for book in readed_books]
    )
    return style,text



@app.callback(
    Output('show_recomendation','style'),
    Output('show_recomendation','children'),
    Input('btn_rec_book','n_clicks'),
    State('show_recomendation','style'),
    prevent_initial_call= True
)

def show_rec(click,style):
    if click % 2 != 0:
        books=book_rec_sys(readed_books)
        book_name= books['Book-Title'].tolist()
        #book_author= books['Book-Author'].tolist()

        text= html.Ul(
            [ html.Li(f'{book_name[i]}',style={"marginBottom": "12px"}) for i in range(len(book_name)) ]
            )
        style['display'] = 'block'

        return style , text
    else:
        style['display'] = 'none'
        return style , ''




if __name__ == '__main__' :
    app.run(debug=True)