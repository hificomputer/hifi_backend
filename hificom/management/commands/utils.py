import yaml


main_categories = [
    {
        'title': 'Laptop',
        'slug': 'laptop',
        'priority': 5,
        'get_features_from_child': True
    },
    {
        'title': 'Desktop',
        'slug': 'desktop',
        'priority': 4,
        'get_features_from_child': True
    },
    {
        'title': 'PC Component',
        'slug': 'pc-component',
        'priority': 4,
    },
    {
        'title': 'Monitor',
        'slug': 'monitor',
        'priority': 4,
        'get_features_from_child': True
    },
    {
        'title': 'Accessories',
        'slug': 'accessories',
        'priority': 3,
    },
    {
        'title': 'Networking',
        'slug': 'networking',
        'priority': 3,
    },
    {
        'title': 'Printer',
        'slug': 'printer',
        'priority': 3,
        'get_features_from_child': True
    },
    {
        'title': 'Office Equipment',
        'slug': 'office-equipment',
        'priority': 3,
    },
    {
        'title': 'Sound System',
        'slug': 'sound-system',
        'priority': 2,
    },
    {
        'title': 'Software',
        'slug': 'software',
        'priority': 2,
    },
]

laptop_subcategories = [
    {
        'title': 'All Laptop',
        'slug': 'all-laptop',
        'priority': 3,
    },
    {
        'title': 'Gaming Laptop',
        'slug': 'gaming-laptop',
        'priority': 2,
    },
    {
        'title': 'Business Laptop',
        'slug': 'business-laptop',
        'priority': 2,
    },
    {
        'title': 'Professional Laptop',
        'slug': 'professional-laptop',
        'priority': 2,
    },
    {
        'title': 'Intel Laptop',
        'slug': 'intel-laptop',
        'priority': 1,
    },
    {
        'title': 'AMD Laptop',
        'slug': 'amd-laptop',
        'priority': 1,
    },
    {
        'title': 'Accessories',
        'slug': 'laptop-accessories',
        'priority': 1,
    },
]

laptop_brands = [
    {
        'title': 'Asus',
        'slug': 'asus',
        'priority': 3,
        'cat_type': 'brand'
    },
    {
        'title': 'Lenovo',
        'slug': 'lenovo',
        'priority': 3,
        'cat_type': 'brand'
    },
    {
        'title': 'HP',
        'slug': 'hp',
        'priority': 3,
        'cat_type': 'brand'
    },
    {
        'title': 'Acer',
        'slug': 'acer',
        'priority': 2,
        'cat_type': 'brand'
    },
    {
        'title': 'Dell',
        'slug': 'dell',
        'priority': 2,
        'cat_type': 'brand'
    },
    {
        'title': 'MSI',
        'slug': 'msi',
        'priority': 2,
        'cat_type': 'brand'
    },
]

laptop_serieses = [
    {
        'title': 'Zenbook',
        'slug': 'zenbook',
        'priority': 1,
        'cat_type': 'series'
    },
    {
        'title': 'Vivobook',
        'slug': 'vivobook',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Expertbook',
        'slug': 'expertbook',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'ROG',
        'slug': 'rog',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'TUF',
        'slug': 'tuf',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Aspire',
        'slug': 'aspire',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Extensa',
        'slug': 'extensa',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Travelmate',
        'slug': 'travelmate',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Yoga',
        'slug': 'yoga',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Thinkpad',
        'slug': 'thinkpad',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Elite',
        'slug': 'elite',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Pavilion',
        'slug': 'pavilion',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Probook',
        'slug': 'probook',
        'priority': 0,
        'cat_type': 'series'
    },
    {
        'title': 'Victus',
        'slug': 'victus',
        'priority': 0,
        'cat_type': 'series'
    },
]

laptop_features = [
    {
        'title': 'OLED Laptop',
        'slug': 'oled-laptop',
        'priority': 3,
        'cat_type': 'feature'
    },
    {
        'title': '4K Laptop',
        'slug': '4k-laptop',
        'priority': 3,
        'cat_type': 'feature'
    },
    {
        'title': '2K Laptop',
        'slug': '2k-laptop',
        'priority': 3,
        'cat_type': 'feature'
    },
    {
        'title': 'QHD Laptop',
        'slug': 'qhd-laptop',
        'priority': 3,
        'cat_type': 'feature'
    },
]

laptop_acceesories = [
    {
        'title': 'Laptop Ram',
        'slug': 'laptop-ram',
        'priority': 3,
    },
    {
        'title': 'Laptop Battery',
        'slug': 'laptop-battery',
        'priority': 3,
    },
    {
        'title': 'Laptop Charger',
        'slug': 'laptop-charger',
        'priority': 3,
    },
    {
        'title': 'Laptop Display',
        'slug': 'laptop-display',
        'priority': 3,
    },
    {
        'title': 'Laptop Cooler',
        'slug': 'laptop-cooler',
        'priority': 3,
    },
    {
        'title': 'Laptop Backpack',
        'slug': 'laptop-backpack',
        'priority': 3,
    },
]

laptop_ram_brands = [
    {
        'title': 'Adata',
        'slug': 'adata-laptop-ram',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'Apacer',
        'slug': 'apacer-laptop-ram',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'Corsair',
        'slug': 'corsair-laptop-ram',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'HP',
        'slug': 'hp-laptop-ram',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'Netac',
        'slug': 'netac-laptop-ram',
        'cat_type': 'brand',
        'priority': 1,
    },
]

laptop_battery_brands = [
    {
        'title': 'Asus',
        'slug': 'asus-laptop-battery',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'Dell',
        'slug': 'dell-laptop-battery',
        'cat_type': 'brand',
        'priority': 1,
    },
]

monitor_brands = [
    {
        'title': 'Dahua',
        'slug': 'dahua-monitor',
        'cat_type': 'brand',
        'priority': 3,
    },
    {
        'title': 'Acer',
        'slug': 'acer-monitor',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'Hikvision',
        'slug': 'hikvision-monitor',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'MSI',
        'slug': 'msi-monitor',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'Viewsonic',
        'slug': 'viewsonic-monitor',
        'cat_type': 'brand',
        'priority': 1,
    },
    {
        'title': 'HP',
        'slug': 'hp-monitor',
        'cat_type': 'brand',
        'priority': 1,
    },
]


all_categories = [
    *main_categories,
    *laptop_subcategories,
    *laptop_brands,
    *laptop_serieses,
    *laptop_features,
    *laptop_acceesories,
    *laptop_ram_brands,
    *laptop_battery_brands,
    *monitor_brands
]

def traverse_cat(cat_tree, parent: str | None = None):
    if type(cat_tree) == list:
        for i in cat_tree:
            if type(i) == dict:
                root = list(i.keys())[0]
                if not len(list(filter(lambda cat: cat['slug'] == root, all_categories))):
                    print(f'{i} Not Found')
                traverse_cat(i[root], root)
            elif type(i) == str:
                if not len(list(filter(lambda cat: cat['slug'] == i, all_categories))):
                    print(f'{i} Not Found')

def browse_yaml(tree):
    for root in tree.keys():
        traverse_cat(tree[root], root)

with open('cat_tree.yaml') as f:
    tree = yaml.load(f, yaml.SafeLoader)
    


if __name__ == "__main__":
    browse_yaml(tree)
