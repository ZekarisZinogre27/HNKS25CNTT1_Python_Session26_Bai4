from abc import ABC, abstractmethod

class Champion(ABC):
    def __init__(self, champion_id, name, base_hp, base_atk):
        if base_hp <= 0:
            base_hp = 100
        if base_atk <= 0:
            base_atk = 100
        self.champion_id = champion_id
        self.name = name
        self.base_hp = base_hp
        self.base_atk = base_atk

    @abstractmethod
    def calculate_skill_damage(self):
        pass

    def get_combat_power(self):
        return self.base_hp + (self.calculate_skill_damage() * 1.5)

    def __add__(self, other):
        if isinstance(other, Champion):
            return self.get_combat_power() + other.get_combat_power()
        return self.get_combat_power() + other

    def __radd__(self, other):
        if other == 0:
            return self.get_combat_power()
        return other + self.get_combat_power()

    def __gt__(self, other):
        return self.get_combat_power() > other.get_combat_power()


class Warrior(Champion):
    def __init__(self, champion_id, name, base_hp, base_atk, shield_bonus):
        Champion.__init__(self, champion_id, name, base_hp, base_atk)
        if shield_bonus <= 0:
            shield_bonus = 100
        self.shield_bonus = shield_bonus

    def calculate_skill_damage(self):
        return self.base_atk * 2 + self.shield_bonus


class Mage(Champion):
    def __init__(self, champion_id, name, base_hp, base_atk, ability_power):
        Champion.__init__(self, champion_id, name, base_hp, base_atk)
        if ability_power <= 0:
            ability_power = 1.0
        self.ability_power = ability_power

    def calculate_skill_damage(self):
        return self.base_atk * self.ability_power

def display_champion_pool(champion_pool):
    print("--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
    print("Mã     | Tên tướng            | Hệ       | HP    | ATK   | Chỉ số riêng      | Chiến lực")
    print("----------------------------------------------------------------------------------------")
    for c in champion_pool:
        combat_power = int(c.get_combat_power())
        if type(c) is Warrior:
            print(c.champion_id.ljust(6) + " | " + c.name.ljust(20) + " | Warrior  | " + str(c.base_hp).ljust(5) + " | " + str(c.base_atk).ljust(5) + " | Armor: " + str(c.shield_bonus).ljust(10) + " | " + str(combat_power))
        elif type(c) is Mage:
            print(c.champion_id.ljust(6) + " | " + c.name.ljust(20) + " | Mage     | " + str(c.base_hp).ljust(5) + " | " + str(c.base_atk).ljust(5) + " | Mana: " + str(c.ability_power).ljust(11) + " | " + str(combat_power))
    print("----------------------------------------------------------------------------------------")
    
def add_new_champion(champion_pool):
    print("[CHỌN HỆ TƯỚNG]: 1. Warrior | 2. Mage")
    sub_choice = int(input("Nhập lựa chọn: "))
    if sub_choice not in [1, 2]:
        print("Lựa chọn hệ tướng không hợp lệ!")
        return
        
    champion_id = input("Nhập mã tướng: ").strip().upper()
    is_duplicate = False
    for c in champion_pool:
        if c.champion_id == champion_id:
            is_duplicate = True
            break
    if is_duplicate:
        print(">> THẤT BẠI: Mã tướng [" + champion_id + "] đã tồn tại!")
        return

    name = input("Nhập tên tướng: ")
    hp = int(input("Nhập HP: "))
    atk = int(input("Nhập ATK: "))
    if sub_choice == 1:
        armor = int(input("Nhập Armor: "))
        new_champ = Warrior(champion_id, name, hp, atk, armor)
        champion_pool.append(new_champ)
        print("Thêm tướng Warrior thành công!")
    elif sub_choice == 2:
        ap = float(input("Nhập hệ số AP: "))
        new_champ = Mage(champion_id, name, hp, atk, ap)
        champion_pool.append(new_champ)
        print("Thêm tướng Mage thành công!")
    print("Mã: " + new_champ.champion_id + " | Tên: " + new_champ.name + " | Chiến lực: " + str(int(new_champ.get_combat_power())))

def compare_two_champions(champion_pool):
    print("--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
    id1 = input("Nhập mã tướng thứ nhất: ").strip().upper()
    id2 = input("Nhập mã tướng thứ hai: ").strip().upper()
    c1 = None
    c2 = None
    
    for c in champion_pool:
        if c.champion_id == id1:
            c1 = c
        if c.champion_id == id2:
            c2 = c
    if c1 is None:
        print("Mã tướng [" + id1 + "] không hợp lệ, bỏ qua!")
        return
    if c2 is None:
        print("Mã tướng [" + id2 + "] không hợp lệ, bỏ qua!")
        return
    print("Thông tin so sánh:")
    print(c1.champion_id + " - " + c1.name + " | Hệ: " + type(c1).__name__ + " | Chiến lực: " + str(int(c1.get_combat_power())))
    print(c2.champion_id + " - " + c2.name + " | Hệ: " + type(c2).__name__ + " | Chiến lực: " + str(int(c2.get_combat_power())))
    print("Kết quả:")
    if c1 > c2:
        print(c1.champion_id + " - " + c1.name + " mạnh hơn " + c2.champion_id + " - " + c2.name + ".")
    elif c2 > c1:
        print(c2.champion_id + " - " + c2.name + " mạnh hơn " + c1.champion_id + " - " + c1.name + ".")
    else:
        print("Hai quân cờ ngang nhau.")

def calculate_lineup_power(champion_pool):
    print("--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---")
    raw_input = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ")
    input_ids = raw_input.split(",")
    
    lineup = []
    for raw_id in input_ids:
        target_id = raw_id.strip().upper()
        found_champ = None
        for c in champion_pool:
            if c.champion_id == target_id:
                found_champ = c
                break
        if found_champ is not None:
            lineup.append(found_champ)
        else:
            print("Mã tướng [" + target_id + "] không hợp lệ, bỏ qua!")
            
    if not lineup:
        print("Đội hình trống hoặc không có tướng nào hợp lệ.")
        return
    print("Danh sách đội hình:")
    
    for idx, c in enumerate(lineup, 1):
        print(str(idx) + ". " + c.champion_id + " - " + c.name + " | Chiến lực: " + str(int(c.get_combat_power())))
    total_power = int(sum(lineup))
    print("Tổng chiến lực đội hình: " + str(total_power))

def main_menu():
    champion_pool = [
        Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
        Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
        Mage("MAG01", "Rikkei Wizard", 800, 500, 1.5)
    ]
    
    while True:
        print("=== QUẢN LÝ ĐỘI HÌNH AUTO-BATTLER ===")
        print("1. Hiển thị bể tướng hiện có")
        print("2. Thêm quân cờ mới")
        print("3. So sánh 2 quân cờ")
        print("4. Tính tổng chiến lực Đội Hình Ra Sân")
        print("5. Thoát chương trình")
        
        try:
            choice = int(input("Chọn chức năng (1-5): "))
            if choice == 1:
                display_champion_pool(champion_pool)
            elif choice == 2:
                add_new_champion(champion_pool)
            elif choice == 3:
                compare_two_champions(champion_pool)
            elif choice == 4:
                calculate_lineup_power(champion_pool)
            elif choice == 5:
                print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
                break
            else:
                print("Vui lòng chọn từ 1 đến 5.") 
        except ValueError:
            print("Vui lòng nhập đúng định dạng số.")
main_menu()