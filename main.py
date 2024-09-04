import flet as ft
import sqlite3
import random

# Connect to SQLite database
con = sqlite3.connect("library.db", check_same_thread=False)
cur = con.cursor()

# Create table if it doesn't exist
cur.execute("CREATE TABLE IF NOT EXISTS Library (id,name, price, copies, author)")

def main(page: ft.Page):
    page.window.width = 250
    page.window.height=600
    page.window.left = 600
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment="center"
    page.vertical_alignment="center"
    page.update()

    def change_screen(e):
        page.snack_bar=ft.SnackBar(ft.Text("scussufle"))
        def len_price(e):
            if t_price.value.isdigit():
                price_er.value=""
            else :
                price_er.value="price should be a number"   
            page.update()
        def len_copies(e):
            if t_copies.value.isdigit():
                copies_er.value=""
            else :
                copies_er.value="copies should be a number"   
            page.update()          
        def len_id(e):
            if t_id.value.isdigit():
                le=len(t_id.value)
                if le != 6:
                    id_er.value="ID should be 6 numbers"
                else:
                    id_er.value=""
            else:
                id_er.value="id should be a number"
            page.update()
        def random_id(e):
            cur.execute("select id from library")
            id=cur.fetchall()
            yes=True
            while yes:
                ran_id=random.randint(100000,999999)
                for x in id:
                    if x[0]==ran_id:
                        continue
                    else:
                        for x in range(1000):
                            t_id.value=""
                            ran=random.randint(100000,999999)
                            t_id.value=str(ran)
                            page.update()
                        t_id.value=str(ran_id)
                        id_er.value=""
                        page.update()
                        yes=False
                        break
        def add_a_book(e):
            if t_name.value!="" and t_author.value!="" and price_er.value=="" and id_er.value=="" and copies_er.value=="" :
                cur.execute("INSERT INTO Library VALUES (?,?, ?, ?, ?)", (t_id.value,t_name.value, t_price.value, t_copies.value, t_author.value))
                con.commit()
                page.update()
                cur.execute("SELECT * FROM Library")
                print(cur.fetchall())
                page.go("/")
            print("123")
        def show_row_data(row_data):
            page.dialog = ft.AlertDialog(
                title=ft.Text("Row Data"),
                content=ft.Text(f"Name: {row_data[0]}\nPrice: {row_data[1]}\nCopies: {row_data[2]}\nAuthor: {row_data[3]}"),
                actions=[ft.TextField()]
            )
            page.dialog.open = True
            page.update()

        # Main buttons
        b_add = ft.ElevatedButton(text="Add a Book", on_click=lambda _: page.go("add"))
        b_list = ft.ElevatedButton(text="List", on_click=lambda _: page.go("list"))
        page.views.append(ft.View("/", [b_add, b_list]))
        page.update()

        if page.route == "add":
            id_er=ft.Text("",color="white",height=18)
            price_er=ft.Text("",color="white",height=18)
            copies_er=ft.Text("",color="white",height=18)
            b_back = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: page.go("/"))
            b_random=ft.ElevatedButton(text="R",on_click=random_id)
            t_id = ft.TextField(label="ID",on_change=len_id)
            t_name = ft.TextField(label="Book Name")
            t_price = ft.TextField(label="Price",on_change=len_price)
            t_copies = ft.TextField(label="Copies")
            t_author = ft.TextField(label="Author Name")
            b_add = ft.ElevatedButton(text='Add', on_click=add_a_book)

            page.views.append(
                ft.View(
                    "add",
                    [b_back, ft.Column(controls=[ft.Row(controls=[t_id,b_random]),id_er,t_name,ft.Divider(height=18,color=ft.colors.BLACK12), t_price,price_er, t_copies,copies_er, t_author, ft.Row(), ft.Row(), b_add])]
                )
            )
            page.update()

        elif page.route == "list":
            def fun(e):
                list_view.controls.clear()
                if search.value=="" or uptodown.value=="all":
                    show_all()
                else:
                    show()
                page.update()
            def show_all():
                cur.execute("SELECT * FROM Library")
                c=cur.fetchall()
                print(c)
                for x in c:
                    b_pop=ft.PopupMenuButton(items=[
                    ft.PopupMenuItem("buy",lambda _,index=x:buy_a_book(index))])
                    row = ft.Row(spacing=20, controls=[ft.Text(x[0]), ft.Text(x[1]), ft.Text(x[2]), ft.Text(x[3]),ft.Text(x[4]),b_pop])
                    list_view.controls.append(row)
            def show():
                cur.execute(f"select {uptodown.value} from Library")
                for x in cur.fetchall():
                    print(x)
                    if str(search.value) in str(x[0]):
                        print("fady")
                        cur.execute(f"select * from Library where {uptodown.value} = ?",(str(x[0]),))
                        i=cur.fetchone()
                        b_pop=ft.PopupMenuButton(items=[ft.PopupMenuItem("buy",lambda _,index=x:buy_a_book(index))])
                        row = ft.Row(spacing=10, controls=[ft.Text(i[0]), ft.Text(i[1]), ft.Text(i[2]), ft.Text(i[3]),ft.Text(i[4]),b_pop])
                        list_view.controls.append(row)
            date_column=ft.Row(spacing=15,controls=[
                ft.Text("ID",width=30),
                ft.Text("name"),
                ft.Text("price"),
                ft.Text("copys"),
                ft.Text("aother")])

            b_back = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: page.go("/"))
            search=ft.TextField(width=150,icon=ft.icons.SEARCH,label="search",height=40,on_change=fun)
            uptodown=ft.Dropdown(width=60,options=[ft.dropdown.Option("all"),ft.dropdown.Option("name"),ft.dropdown.Option("copies"),ft.dropdown.Option("price"),ft.dropdown.Option("aothur"),])
            uptodown.value="all"
            list_view = ft.ListView(spacing=10)
            fun("")

            page.views.append(ft.View("list", [b_back,ft.Row(spacing=10,controls=[search,uptodown]),date_column, list_view]))
            page.update()

    page.on_route_change = change_screen
    page.go("/")

ft.app(target=main)
