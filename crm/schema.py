import graphene
from graphene_django.types import DjangoObjectType
from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal
from .models import Customer, Product, Order


# Django Object Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


# Input Types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)  # Changed back to Float for easier input
    stock = graphene.Int()


class OrderInput(graphene.InputObjectType):
    customerId = graphene.ID(required=True)  # Changed to match checkpoint format
    productIds = graphene.List(graphene.ID, required=True)  # Changed to match checkpoint format
    order_date = graphene.DateTime()


# Custom Error Type
class ErrorType(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()


# Mutation Response Types
# class CreateCustomer(graphene.Mutation)
class CreateCustomerMutation(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, input):
        try:
            # Check if email already exists
            if Customer.objects.filter(email=input.email).exists():
                return CreateCustomerMutation(
                    errors=[ErrorType(field="email", message="Email already exists")]
                )
            
            # Validate phone format if provided
            if input.phone:
                customer = Customer(name=input.name, email=input.email, phone=input.phone)
                customer.full_clean()  # This will validate the phone regex
            else:
                customer = Customer(name=input.name, email=input.email)
                customer.full_clean()
            
            customer.save()
            return CreateCustomerMutation(
                customer=customer,
                message=f"Customer '{customer.name}' created successfully!"
            )
        except ValidationError as e:
            errors = []
            for field, messages in e.message_dict.items():
                for message in messages:
                    # Provide user-friendly error messages
                    if field == 'email' and 'unique' in message.lower():
                        errors.append(ErrorType(field=field, message="Email already exists"))
                    elif field == 'phone':
                        errors.append(ErrorType(field=field, message="Invalid phone format. Use +1234567890 or 123-456-7890"))
                    else:
                        errors.append(ErrorType(field=field, message=message))
            return CreateCustomerMutation(errors=errors)
        except Exception as e:
            return CreateCustomerMutation(
                errors=[ErrorType(field="general", message=str(e))]
            )


class BulkCreateCustomersMutation(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, input):
        customers_created = []
        errors = []
        
        # Process each customer individually (not in a single transaction for partial success)
        for i, customer_input in enumerate(input):
            try:
                # Check if email already exists
                if Customer.objects.filter(email=customer_input.email).exists():
                    errors.append(ErrorType(
                        field=f"customer_{i}_email",
                        message="Email already exists"
                    ))
                    continue
                
                if customer_input.phone:
                    customer = Customer(
                        name=customer_input.name,
                        email=customer_input.email,
                        phone=customer_input.phone
                    )
                else:
                    customer = Customer(
                        name=customer_input.name,
                        email=customer_input.email
                    )
                
                customer.full_clean()
                customer.save()
                customers_created.append(customer)
                
            except ValidationError as e:
                for field, messages in e.message_dict.items():
                    for message in messages:
                        # Provide user-friendly error messages
                        if field == 'email' and 'unique' in message.lower():
                            error_message = "Email already exists"
                        elif field == 'phone':
                            error_message = "Invalid phone format. Use +1234567890 or 123-456-7890"
                        else:
                            error_message = message
                        
                        errors.append(ErrorType(
                            field=f"customer_{i}_{field}",
                            message=error_message
                        ))
            except Exception as e:
                errors.append(ErrorType(
                    field=f"customer_{i}",
                    message=str(e)
                ))
        
        return BulkCreateCustomersMutation(customers=customers_created, errors=errors)


class CreateProductMutation(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, input):
        try:
            # Convert price float to Decimal and validate it's positive
            try:
                price = Decimal(str(input.price))
            except (ValueError, TypeError):
                return CreateProductMutation(
                    errors=[ErrorType(field="price", message="Invalid price format")]
                )
            
            if price <= 0:
                return CreateProductMutation(
                    errors=[ErrorType(field="price", message="Price must be positive")]
                )
            
            # Validate stock is non-negative (allow 0)
            stock = input.stock if input.stock is not None else 0
            if stock < 0:
                return CreateProductMutation(
                    errors=[ErrorType(field="stock", message="Stock must be non-negative (0 or greater)")]
                )
            
            product = Product(
                name=input.name,
                price=price,  # Use the converted Decimal value
                stock=stock
            )
            product.full_clean()
            product.save()
            
            return CreateProductMutation(product=product)
            
        except ValidationError as e:
            errors = []
            for field, messages in e.message_dict.items():
                for message in messages:
                    errors.append(ErrorType(field=field, message=message))
            return CreateProductMutation(errors=errors)
        except Exception as e:
            return CreateProductMutation(
                errors=[ErrorType(field="general", message=str(e))]
            )


class CreateOrderMutation(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, input):
        try:
            # Validate customer exists
            try:
                customer = Customer.objects.get(id=input.customerId)
            except Customer.DoesNotExist:
                return CreateOrderMutation(
                    errors=[ErrorType(field="customerId", message="Customer does not exist")]
                )
            
            # Validate products exist and at least one is selected
            if not input.productIds:
                return CreateOrderMutation(
                    errors=[ErrorType(field="productIds", message="At least one product must be selected")]
                )
            
            products = []
            invalid_product_ids = []
            
            for product_id in input.productIds:
                try:
                    product = Product.objects.get(id=product_id)
                    products.append(product)
                except Product.DoesNotExist:
                    invalid_product_ids.append(product_id)
            
            if invalid_product_ids:
                return CreateOrderMutation(
                    errors=[ErrorType(
                        field="productIds",
                        message=f"Invalid product IDs: {', '.join(invalid_product_ids)}"
                    )]
                )
            
            # Create order
            with transaction.atomic():
                order = Order(customer=customer)
                if input.order_date:
                    order.order_date = input.order_date
                
                order.save()
                order.products.set(products)
                
                # Calculate total amount
                total = sum(product.price for product in products)
                order.total_amount = total
                order.save(update_fields=['total_amount'])
            
            return CreateOrderMutation(order=order)
            
        except Exception as e:
            return CreateOrderMutation(
                errors=[ErrorType(field="general", message=str(e))]
            )


# Query class
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)
    customer = graphene.Field(CustomerType, id=graphene.ID(required=True))
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    order = graphene.Field(OrderType, id=graphene.ID(required=True))

    def resolve_all_customers(self, info):
        return Customer.objects.all()

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_all_orders(self, info):
        return Order.objects.all()

    def resolve_customer(self, info, id):
        try:
            return Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return None

    def resolve_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    def resolve_order(self, info, id):
        try:
            return Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return None


# Mutation class
class Mutation(graphene.ObjectType):
    #create_customer = CreateCustomer.Field()
    create_customer = CreateCustomerMutation.Field()
    bulk_create_customers = BulkCreateCustomersMutation.Field()
    create_product = CreateProductMutation.Field()
    create_order = CreateOrderMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)