def filtrar_por_product_name(products, nome):
    lista_filtrada_por_product_name = []

    for product in products:
        if product['nome'].lower() == nome.lower():
            lista_filtrada_por_product_name.append(product)

    return lista_filtrada_por_product_name

def filtrar_por_product_description(products, descricao):
    lista_filtrada_por_product_description = []

    for product in products:
        if product['descricao'].lower() == descricao.lower():
            lista_filtrada_por_product_description.append(product)

    return lista_filtrada_por_product_description

def filtrar_por_product_price(products, preco):
    lista_filtrada_por_product_price = []

    for product in products:
        if product['preco'].lower() == preco.lower():
            lista_filtrada_por_product_price.append(product)

        return lista_filtrada_por_product_price

def filtrar_por_product_photo(products, foto):
    lista_filtrada_por_product_photo = []

    for product in products:
        if product['foto'].lower() == foto.lower():
            lista_filtrada_por_product_photo.append(product)

        return lista_filtrada_por_product_photo

def filtrar_por_stock_quantity(products, quantidade):
    lista_filtrada_por_stock_quantity = []

    for product in products:
        if product['quantidade'].lower() == quantidade.lower():
            lista_filtrada_por_stock_quantity.append(product)

        return lista_filtrada_por_stock_quantity
