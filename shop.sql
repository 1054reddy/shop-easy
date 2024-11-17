CREATE DATABASE fashionwebsite;

USE fashionwebsite;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    address VARCHAR(255),
    mobile_no VARCHAR(15),
    gender VARCHAR(10),
    age INT
);

CREATE TABLE Admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100),
    admin_id INT,
    FOREIGN KEY (admin_id) REFERENCES Admins(admin_id)
);

CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price FLOAT,
    category_id INT,
    admin_id INT,
    stock_quantity INT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (admin_id) REFERENCES Admins(admin_id)
);

CREATE TABLE Product_Sizes (
    product_size_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    size VARCHAR(10),
    stock_quantity INT,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATE,
    total_amount FLOAT,
    tracking_number VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Order_Items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    product_size_id INT,
    quantity INT,
    price FLOAT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (product_size_id) REFERENCES Product_Sizes(product_size_id)
);

CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    rating INT,
    comment TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Carts (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Cart_Items (
    cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT,
    product_id INT,
    product_size_id INT,
    quantity INT,
    price FLOAT,
    FOREIGN KEY (cart_id) REFERENCES Carts(cart_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (product_size_id) REFERENCES Product_Sizes(product_size_id)
);


INSERT INTO Admins (admin_id, admin_name, email, password)
VALUES 
    (1, 'Raja Reddy', 'reddyraja1366@gmail.com', 'raja@1366'); -- Change values as needed

INSERT INTO Categories (category_id, category_name, admin_id)
VALUES 
    (1, 'Men\'s Fashion', 1), 
    (2, 'Women\'s Fashion', 1), 
    (3, 'Kids\' Fashion', 1), 
    (4, 'Accessories', 1), 
    (5, 'Bags', 1), 
    (6, 'Electronics', 1); 

-- Inserting into Products table
INSERT INTO Products (product_id, name, description, price, category_id, admin_id, stock_quantity)
VALUES 
(1, "Men's T-Shirt", "A comfortable and stylish men's t-shirt made from 100% cotton.", 19.99, 1, 1, 50),
(2, "Women's Dress", "A stylish and elegant women's dress suitable for any occasion.", 29.99, 2, 1, 30),
(3, "Kids' Shoes", "Durable and comfortable shoes designed for active kids.", 24.99, 3, 1, 40),
(4, "Classic Watch", "A classy watch that goes well with both formal and casual wear.", 99.99, 4, 1, 20),
(5, "Leather Backpack", "A spacious leather backpack perfect for school or travel.", 49.99, 5, 1, 15),
(6, "Wireless Headphones", "Noise-cancelling wireless headphones with superior sound quality.", 79.99, 6, 1, 25),
(7, "Casual Sneakers", "Comfortable and trendy casual sneakers for everyday wear.", 54.99, 4, 1, 35),
(8, "Fitness Tracker", "Track your workouts and daily activity with this smart fitness tracker.", 39.99, 6, 1, 45),
(9,"Jeans for Men","Men Grey Tapered Fit Mid-Rise Clean Look Stretchable Jeans",24.99,1,1,40),
(10,"Hooded Sweatshirt","Men Black Striped Slim Fit Hooded Sweatshirt",29.99,1,1,30),
(11,"Formal Blazzer","Single Breasted Formal Blazer",39.99,1,1,20),
(12,"Kurta for Men","Men Purple Ethnic Motifs Embroidered Thread Work Pure Cotton Kurta",29.99,1,1,20),
(13,"Kurta Set for Women","Ethnic Motifs Printed V-Neck Pure Cotton A-Line Kurta with Palazzos & Dupatta",24.99,2,1,30),
(14,"Saree","Embroidered Net Saree",29.99,2,1,20),
(15,"Formal Blazzer","Corduroy Single-Breasted Blazer",34.99,2,1,15),
(16,"Body Con","Black Net Ruched Bodycon Dress",29.99,2,1,20),
(17,"Top for Women","Floral Print Mandarin Collar Puff Sleeve Cotton Peplum Top",19.99,2,1,20),
(18,"T-Shirt for Kids","Boys White Spider-Man Printed T-shirt",6.99,3,1,20),
(19,"Shirt for Kids","Boys Spread Collar Solid Cotton Casual Shirt",9.99,3,1,15),
(20,"Girl Dresses","Girls Ruffles Fit & Flare Dress",7.99,3,1,20),
(21,"Wallet for Men","Men Solid Brown Wallets with RFID Features",14.99,4,1,15),
(22,"Belt for Men","Men Reversible Textured Belt",12.99,4,1,10),
(23,"Watch for Women","Women Black Dial & Bracelet Style Analogue Watch",34.99,4,1,30),
(24,"Sneakers for Women","Air Jordan 1 Low Women's Shoes",150,2,1,20),
(25,"Bag","Geometric Printed Structured Tote Bag With Pouch",20,5,1,20),
(26,"Air Pods","AirPods 4 with Active Noise Cancellation",150,6,1,25),
(27,"Ipad","Apple iPad (10th Generation)",600,6,1,20);

-- Inserting into Product_Sizes table
INSERT INTO Product_Sizes (product_id, size, stock_quantity)
VALUES
(1, 'S', 10),
(1, 'M', 10),
(1, 'L', 10),
(1, 'XL', 10),
(2, 'S', 8),
(2, 'M', 8),
(2, 'L', 8),
(3, 'S', 12),
(3, 'M', 12),
(7, 'M', 10),
(7, 'L', 10),
(9,'S',10),
(9,'M',10),
(9,'L',10),
(9,'XL',10),
(10,'S',10),
(10,'M',10),
(10,'L',5),
(10,'XL',5),
(11,'S',5),
(11,'M',5),
(11,'L',5),
(11,'XL',5),
(12,'S',5),
(12,'M',5),
(12,'L',5),
(12,'XL',5),
(13,'S',10),
(13,'M',10),
(13,'L',10),
(14,'One Size',20),
(15,'S',5),
(15,'M',5),
(15,'L',5),
(16,'S',5),
(16,'M',5),
(16,'L',5),
(16,'XL',5),
(17,'S',5),
(17,'M',5),
(17,'L',5),
(17,'XL',5),
(18,'One Size',20),
(19,'One Size',15),
(20,'One Size',20),
(21,'One Size',15),
(22,'One Size',10),
(23,'One Size',30),
(24,'5',5),
(24,'6',5),
(24,'7',5),
(24,'8',5),
(25,'One Size',20),
(26,'One Size',25),
(27,'One Size',25);
INSERT INTO Product_Sizes (product_id, size, stock_quantity)
VALUES
(4,'One size',30),
(5,'S',20),
(5,'M',20),
(5,'L',20),
(6,'One size',30),
(8,'One size',30);
ALTER TABLE Users MODIFY password VARCHAR(255);
ALTER TABLE Products ADD FULLTEXT(name, description);
ALTER TABLE Orders ADD COLUMN order_status VARCHAR(50);
UPDATE Orders
SET tracking_number = CONCAT('TRK', LPAD(order_id, 6, '0'))
WHERE order_id = LAST_INSERT_ID();


DELIMITER $$

CREATE TRIGGER prevent_duplicate_cart_item
BEFORE INSERT ON Cart_Items
FOR EACH ROW
BEGIN
    DECLARE item_exists INT;
    
    -- Check if the product with the same size is already in the cart
    SELECT COUNT(*) INTO item_exists
    FROM Cart_Items
    WHERE cart_id = NEW.cart_id
    AND product_id = NEW.product_id
    AND product_size_id = NEW.product_size_id;
    
    IF item_exists > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Product with the same size already exists in the cart';
    END IF;
END $$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER update_product_stock_after_order
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    -- Decrease the stock quantity in the Product_Sizes table after an order is placed
    UPDATE Product_Sizes
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE product_size_id = NEW.product_size_id;
    
    -- Ensure stock doesn't go below zero
    IF (SELECT stock_quantity FROM Product_Sizes WHERE product_size_id = NEW.product_size_id) < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock for the ordered product size';
    END IF;
END $$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER prevent_negative_stock
BEFORE UPDATE ON Product_Sizes
FOR EACH ROW
BEGIN
    IF NEW.stock_quantity < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock quantity cannot be negative';
    END IF;
END $$

DELIMITER ;

CREATE TABLE Order_Status_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

DELIMITER $$

CREATE TRIGGER log_order_status_update
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
    -- Log status changes
    IF OLD.tracking_number != NEW.tracking_number THEN
        INSERT INTO Order_Status_Log (order_id, old_status, new_status)
        VALUES (NEW.order_id, OLD.tracking_number, NEW.tracking_number);
    END IF;
END $$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER restore_stock_on_order_cancel
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
    -- Declare the necessary variables and cursor at the start
    DECLARE product_size_id INT;
    DECLARE order_quantity INT;
    DECLARE cur CURSOR FOR 
        SELECT product_size_id, quantity 
        FROM Order_Items 
        WHERE order_id = NEW.order_id;
    
    -- Declare an exit handler to handle cursor closure in case of an error
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET product_size_id = NULL;

    -- Check if the order is canceled
    IF NEW.order_status = 'Canceled' THEN
        OPEN cur;
        
        -- Fetch the first row from the cursor
        FETCH cur INTO product_size_id, order_quantity;
        
        -- Loop through all the rows in the cursor
        WHILE product_size_id IS NOT NULL DO
            -- Restore the stock quantity in Product_Sizes for the canceled order
            UPDATE Product_Sizes
            SET stock_quantity = stock_quantity + order_quantity
            WHERE product_size_id = product_size_id;
            
            -- Fetch the next row from the cursor
            FETCH cur INTO product_size_id, order_quantity;
        END WHILE;
        
        -- Close the cursor after use
        CLOSE cur;
    END IF;
END $$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER update_stock_on_cart_removal
AFTER DELETE ON Cart_Items
FOR EACH ROW
BEGIN
    -- Increase the stock in Product_Sizes when an item is removed from the cart
    UPDATE Product_Sizes
    SET stock_quantity = stock_quantity + OLD.quantity
    WHERE product_size_id = OLD.product_size_id;
END $$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER log_user_updates
AFTER UPDATE ON Users
FOR EACH ROW
BEGIN
    INSERT INTO User_Update_Log (user_id, old_name, new_name, old_email, new_email, updated_at)
    VALUES (NEW.user_id, OLD.name, NEW.name, OLD.email, NEW.email, NOW());
END $$

DELIMITER ;

select*from Users;
select*from Products;
select*from Carts;
select*from Cart_Items;
select* from Product_Sizes;

SHOW INDEX FROM Products;

