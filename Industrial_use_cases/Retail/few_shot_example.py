few_shots = [
    {
        "Question": "How many t-shirts do we have left for Nike in small size and white color?",
        "SQLQuery": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'S'",
        "SQLResult": "Result of the SQL query",
        "Answer": "90",
    },
    {
        "Question": "How many t-shirts do we have left for Nike in extra small size and white color?",
        "SQLQuery": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
        "SQLResult": "Result of the SQL query",
        "Answer": "0",
    },
    {
        "Question": "How many t-shirts of Nike are left in the store?",
        "SQLQuery": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike'",
        "SQLResult": "Result of the SQL query",
        "Answer": '517',
    },
    {
        "Question": "How much is the price of the inventory for all small size t-shirts?",
        "SQLQuery": "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
        "SQLResult": "Result of the SQL query",
        "Answer": "20985",
    },
    {
        "Question": "If we have to sell all the Adidas T-shirts today with discounts applied. How much revenue my store will generate (post discounts)?",
        "SQLQuery": """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
        (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Adidas'
        group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
        """,
        "SQLResult": "Result of the SQL query",
        "Answer": "28710.2",
    },
    {
        "Question": "If we have to sell all the Levi's T-shirts today. How much revenue our store will generate without discount?",
        "SQLQuery": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
        "SQLResult": "Result of the SQL query",
        "Answer": "21473",
    },
    {
        "Question": "How many white color Levi's t-shirts we have available?",
        "SQLQuery": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
        "SQLResult": "Result of the SQL query",
        "Answer": "196",
    }
]