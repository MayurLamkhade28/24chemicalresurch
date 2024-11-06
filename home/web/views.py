from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Title, Datatable, Category, Report_price, Cart


class HomeView(View):
    def get(self, request):
        titles = Title.objects.all()  # Fetch all reports
        return render(request, 'index.html', {'titles': titles})


class ReportDetailView(View):
    def get(self, request, rep_id, url_slug):
        title = get_object_or_404(Title, rep_id=rep_id)
        datatable = get_object_or_404(Datatable, rep_id=rep_id)
        category = get_object_or_404(Category, rep_category_id=title.rep_category_id)
        buying_options = Report_price.objects.all()

        context = {
            'title': title,
            'datatable': datatable,
            'category_name': category.category_name,
            'buying_options': buying_options
        }

        return render(request, 'info.html', context)


class AddCartView(View):
    def post(self, request, rep_id, ):
        print(rep_id)
        pass
        # report = get_object_or_404(Title, rep_id=rep_id)
        # price_option = get_object_or_404(Report_price, price_id=price_id)
        # print("in AddCartView")

        # cart_item = {
        #     "rep_id": report.rep_id,
        #     "rep_title": report.rep_title,
        #     "license": price_option.label,
        #     "price": price_option.price,
        # }

        # print(f"Adding to cart: Report ID: {report.rep_id}, Title: {report.rep_title}, License: {price_option.label}, Price: {price_option.price}")

        # if "cart" not in request.session:
        #     request.session["cart"] = []

        # if cart_item not in request.session["cart"]:
        #     request.session["cart"].append(cart_item)
        #     request.session.modified = True

        # Cart.objects.update_or_create(id=1, defaults={"cart_data": request.session["cart"]})

        return render(request, 'cart.html')


class CartView(View):
    def get(self, request):
        cart_items = request.session.get("cart", [])
        print("Session Cart Items Retrieved: ", cart_items)

        if not cart_items:
            try:
                db_cart_data = Cart.objects.get(id=1).cart_data
                request.session["cart"] = db_cart_data
                request.session.modified = True
            except Cart.DoesNotExist:
                db_cart_data = []

        return render(request, 'cart.html', {"cart_items": cart_items})

    def post(self, request):
        rep_id = request.POST.get("rep_id")
        cart_items = request.session.get("cart")
        updated_cart = [item for item in cart_items if str(item["rep_id"]) != rep_id]
        request.session["cart"] = updated_cart
        request.session.modified = True

        Cart.objects.update_or_create(id=1, defaults={"cart_data": updated_cart})
        print("Updated Cart Items After Removal:", request.session["cart"])
        return redirect('cart_view')
