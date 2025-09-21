-- Категории товаров
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Дерево категорий
CREATE TABLE category_closure (
    ancestor_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    descendant_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    depth INT NOT NULL,
    PRIMARY KEY (ancestor_id, descendant_id)
);

CREATE INDEX idx_category_closure_desc ON category_closure(descendant_id);
CREATE INDEX idx_category_closure_ancestor ON category_closure(ancestor_id);

-- Номенклатура
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku TEXT UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    quantity INT NOT NULL DEFAULT 0,
    price NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_products_sku ON products(sku);

-- Связь товаров с категориями
CREATE TABLE product_categories (
    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    category_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, category_id)
);

CREATE INDEX idx_product_categories_category ON product_categories(category_id);

-- Клиенты
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    contact_phone TEXT,
    contact_email TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_clients_email ON clients(contact_email);
CREATE INDEX idx_clients_phone ON clients(contact_phone);

-- Заказы
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(id),
    order_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
    status TEXT NOT NULL DEFAULT 'new',
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    shipping_address TEXT
);

CREATE INDEX idx_orders_client ON orders(client_id);

-- Детали заказа
CREATE TABLE order_items (
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    price_at_order NUMERIC(12,2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

CREATE INDEX idx_order_items_product ON order_items(product_id);
