import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from store.models import UserProfiles, Order, Inventory,  Material

### ------------------- DASHBOARD -------------------

def dashboard(request):
    total_orders = Order.objects.count()
    active_orders = Order.objects.filter(status="Active").count()
    inventory_warnings = Material.objects.filter(quantity__lt=5).count()

    context = {
        "total_orders": total_orders,
        "active_orders": active_orders,
        "inventory_warnings": inventory_warnings,
    }
    return render(request, "dashboard.html", context)



### ------------------- USER MANAGEMENT -------------------

def user_management_view(request):
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")

    users = User.objects.all()
    if search:
        users = users.filter(username__icontains=search) | users.filter(email__icontains=search)
    if status:
        is_active = status.lower() == "active"
        users = users.filter(is_active=is_active)

    return render(request, "users/user_list.html", {"users": users})


def user_edit_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(UserProfiles, user=user)

    if request.method == "POST":
        user.email = request.POST.get("email")
        user.save()
        profile.Address = request.POST.get("address")
        profile.Phone = request.POST.get("phone")
        profile.save()
        messages.success(request, "User updated.")
        return redirect("user_management")

    return render(request, "users/user_edit.html", {"user": user, "profile": profile})


def user_disable_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    messages.success(request, "User disabled.")
    return redirect("user_management")


def user_invite_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfiles.objects.create(user=user)
        messages.success(request, "User invited.")
        return redirect("user_management")
    return render(request, "users/user_invite.html")


### ------------------- ORDER MANAGEMENT -------------------

def order_management_view(request):
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")
    material = request.GET.get("material", "")
    priority = request.GET.get("priority", "")

    orders = Order.objects.all()

    if search:
        orders = orders.filter(model_name__icontains=search) | orders.filter(id__icontains=search)
    if status:
        orders = orders.filter(status__iexact=status)
    if material:
        orders = orders.filter(material__name__icontains=material)
    if priority:
        orders = orders.filter(priority__iexact=priority)

    return render(request, "orders/order_list.html", {"orders": orders})


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "orders/order_detail.html", {"order": order})


def order_edit_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        order.status = request.POST.get("status")
        order.priority = request.POST.get("priority")
        order.save()
        messages.success(request, "Order updated.")
        return redirect("order_management")
    return render(request, "orders/order_edit.html", {"order": order})


def order_delete_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    messages.success(request, "Order deleted.")
    return redirect("order_management")


### ------------------- INVENTORY MANAGEMENT -------------------

def inventory_management_view(request):
    search = request.GET.get("search", "")
    material = request.GET.get("material", "")
    min_quantity = request.GET.get("min_quantity", "")

    inventory = Inventory.objects.all()

    if search:
        inventory = inventory.filter(material_name__icontains=search)
    if material:
        inventory = inventory.filter(material_name__icontains=material)
    if min_quantity:
        inventory = inventory.filter(quantity__gte=int(min_quantity))

    return render(request, "inventory/inventory_list.html", {"inventory": inventory})


def inventory_edit_view(request, inventory_id):
    item = get_object_or_404(Inventory, pk=inventory_id)
    if request.method == "POST":
        item.material_name = request.POST.get("material_name")
        item.quantity = request.POST.get("quantity")
        item.save()
        messages.success(request, "Inventory updated.")
        return redirect("inventory_management")
    return render(request, "inventory/inventory_edit.html", {"item": item})


def inventory_delete_view(request, inventory_id):
    item = get_object_or_404(Inventory, pk=inventory_id)
    item.delete()
    messages.success(request, "Inventory item deleted.")
    return redirect("inventory_management")


### ------------------- CSV UPLOAD -------------------

@require_http_methods(["GET", "POST"])
def csv_upload_view(request):
    if request.method == "POST":
        upload_type = request.POST.get("upload_type")
        validate = request.POST.get("validate", None)
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            messages.error(request, "No file selected.")
            return redirect("csv_upload")

        if not validate:
            messages.error(request, "Please validate before uploading")
            return redirect("csv_upload")

        try:
            decoded_file = uploaded_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)

            if upload_type == "users":
                for row in reader:
                    if "username" not in row or "email" not in row:
                        raise ValueError("Missing required fields")
                    User.objects.create_user(
                        username=row["username"],
                        email=row["email"],
                        password=row.get("password", "defaultpassword")
                    )
                messages.success(request, "Users uploaded successfully.")
            else:
                messages.error(request, "Unknown upload type.")
        except Exception as e:
            messages.error(request, f"Invalid CSV: {str(e)}")

        return redirect("csv_upload")

    return render(request, "csv/csv_upload.html")


def sample_csv_download_view(request, upload_type):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{upload_type}_sample.csv"'
    writer = csv.writer(response)

    if upload_type == "users":
        writer.writerow(["username", "email", "password"])
        writer.writerow(["user1", "user1@example.com", "password123"])
    else:
        writer.writerow(["invalid_type"])
    return response
