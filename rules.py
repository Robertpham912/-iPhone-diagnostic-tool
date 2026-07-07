# -*- coding: utf-8 -*-
"""
Cay luat chan doan iPhone.
Moi "problem" co: id, name, category, auto_test (hoac None), tree (cay cau hoi).
Node cua tree la mot trong hai dang:
  - {"question": str, "options": [{"label": str, "next": Node}, ...]}
  - {"diagnosis": {"title": str, "severity": "ok"|"warning"|"critical",
                   "explanation": str, "steps": [str, ...], "service": bool}}
"""

def diag(title, severity, explanation, steps, service=False):
    return {"diagnosis": {
        "title": title,
        "severity": severity,
        "explanation": explanation,
        "steps": steps,
        "service": service,
    }}


def q(question, options):
    return {"question": question, "options": options}


PROBLEMS = {

    # ---------------- HARDWARE ----------------

    "battery": {
        "name": "Pin tut nhanh / sac cham",
        "category": "hardware",
        "auto_test": "battery",
        "tree": q(
            "May co nong bat thuong khi sac khong?",
            [
                {"label": "Co, kha nong", "next": q(
                    "Cau/sac dang dung co phai chinh hang (hoac MFi) khong?",
                    [
                        {"label": "Khong chac / hang troi noi", "next": diag(
                            "Nhieu kha nang do phu kien sac khong dat chuan",
                            "warning",
                            "Sac/cap khong chinh hang co the sac cham, khong on dinh dong dien va lam may nong hon binh thuong.",
                            [
                                "Doi sang cap va cu sac chinh hang hoac co chung nhan MFi.",
                                "Khong dung may khi dang sac neu thay nong bat thuong.",
                                "Kiem tra cong sac xem co bui/nuoc khong, ve sinh nhe bang co mem.",
                            ],
                        )},
                        {"label": "Co, hang chinh hang", "next": diag(
                            "Co the pin da chai hoac loi cam bien nhiet",
                            "warning",
                            "Neu dung phu kien chinh hang ma van nong bat thuong, kha nang la dung luong pin (battery health) da giam sau hoac co van de phan cung ben trong.",
                            [
                                "Vao Cai dat > Pin > Tinh trang pin & sac de xem % dung luong toi da.",
                                "Neu duoi 80%, nen can nhac thay pin tai co so uy tin / Apple.",
                                "Trong luc cho, tranh sac qua dem lien tuc va tranh de may o nhiet do cao.",
                            ],
                            service=True,
                        )},
                    ],
                )},
                {"label": "Khong, binh thuong", "next": q(
                    "May co nhieu app chay ngam / lam moi nen thuong xuyen khong?",
                    [
                        {"label": "Co kha nhieu app", "next": diag(
                            "Hao pin do phan mem (background activity)",
                            "ok",
                            "Nhieu app lam moi noi dung ngam hoac dinh vi lien tuc la nguyen nhan pho bien khien pin tut nhanh, khong lien quan phan cung.",
                            [
                                "Vao Cai dat > Tong quat > Lam moi noi dung nen, tat bot app khong can thiet.",
                                "Vao Cai dat > Quyen rieng tu & Bao mat > Dich vu dinh vi, gioi han app dung GPS ngam.",
                                "Kiem tra Cai dat > Pin de xem app nao ngon pin nhat va can nhac go/gioi han.",
                            ],
                        )},
                        {"label": "Khong nhieu", "next": diag(
                            "Co the pin da lao hoa tu nhien",
                            "warning",
                            "Neu da loai tru phu kien va app ngam, pin tut nhanh thuong do dung luong pin giam theo thoi gian su dung.",
                            [
                                "Kiem tra Cai dat > Pin > Tinh trang pin & sac.",
                                "Neu dung luong toi da duoi 80%, nen thay pin.",
                                "Bat che do Low Power Mode de keo dai thoi gian dung trong luc cho thay.",
                            ],
                            service=True,
                        )},
                    ],
                )},
            ],
        ),
    },

    "screen": {
        "name": "Man hinh (cham khong nhay / vet la / mo)",
        "category": "hardware",
        "auto_test": "touch",
        "tree": q(
            "Van de xay ra o mot vung co dinh tren man hinh hay toan bo man hinh?",
            [
                {"label": "Mot vung co dinh", "next": q(
                    "May co tung bi roi, va dap, hoac dinh nuoc gan day khong?",
                    [
                        {"label": "Co", "next": diag(
                            "Nghi ngo hong phan cung do va dap / vao nuoc",
                            "critical",
                            "Loi cham/hinh anh chi xay ra o mot vung co dinh sau khi va dap hoac dinh nuoc thuong la dau hieu man hinh hoac cap ket noi ben trong bi anh huong vat ly.",
                            [
                                "Ngung dung luc man hinh am uot (neu co) va de may kho tu nhien, khong sac ngay.",
                                "Khong tu y thao may de tranh hong them.",
                                "Mang den trung tam bao hanh / sua chua uy tin de kiem tra phan cung.",
                            ],
                            service=True,
                        )},
                        {"label": "Khong", "next": diag(
                            "Co the loi diem anh hoac lop cam ung cuc bo",
                            "warning",
                            "Vung loi co dinh khong ro nguyen nhan va dap co the la diem anh chet hoac lop cam ung bi lao hoa cuc bo.",
                            [
                                "Thu khoi dong lai may (tat nguon, bat lai).",
                                "Kiem tra bang cach chay test mau/cham o cong cu nay de xac dinh ranh gioi vung loi.",
                                "Neu van con sau khoi dong lai, nen mang di kiem tra phan cung.",
                            ],
                            service=True,
                        )},
                    ],
                )},
                {"label": "Toan bo man hinh", "next": diag(
                    "Co the loi phan mem hoac driver cam ung toan cuc",
                    "warning",
                    "Loi anh huong toan bo man hinh thuong lien quan phan mem (can cap nhat/khoi dong lai) hon la mot diem hong vat ly don le.",
                    [
                        "Khoi dong lai may hoan toan (khong chi khoa man hinh).",
                        "Vao Cai dat > Tong quat > Cap nhat phan mem, cap nhat len ban moi nhat.",
                        "Neu van con loi sau khi cap nhat, thu Khoi dong o che do an toan hoac khoi phuc tu ban sao luu.",
                    ],
                )},
            ],
        ),
    },

    "audio": {
        "name": "Loa / Mic (am thanh nho, re, khong nghe ro)",
        "category": "hardware",
        "auto_test": "audio",
        "tree": q(
            "Van de xay ra voi loa (nghe), mic (noi), hay ca hai?",
            [
                {"label": "Chi loa", "next": diag(
                    "Nghi ngo bui/vai loa hoac loi phan mem am luong",
                    "warning",
                    "Am thanh nho hoac re thuong do bui ket o luoi loa, hoac che do am thanh/gioi han am luong dang bat.",
                    [
                        "Kiem tra Cai dat > Am thanh & Xuc giac, tat 'Gioi han am luong toi da' neu dang bat.",
                        "Dung ban chai mem/tam co lam sach nhe luoi loa o day may.",
                        "Thu phat am thanh qua tai nghe de loai tru loi phan mem; neu tai nghe van nho, kha nang loa vat ly bi hong.",
                    ],
                    service=True,
                )},
                {"label": "Chi mic", "next": diag(
                    "Nghi ngo quyen truy cap mic hoac vat can vat ly",
                    "warning",
                    "Mic khong thu duoc am hoac nho co the do ung dung chua duoc cap quyen mic, hoac lo mic bi che/bui.",
                    [
                        "Vao Cai dat > Quyen rieng tu & Bao mat > Microphone, kiem tra app dang dung co duoc bat quyen khong.",
                        "Kiem tra op lung/mieng dan man hinh co dang che lo mic khong.",
                        "Dung tinh nang ghi am co san de test truc tiep truoc khi ket luan hong phan cung.",
                    ],
                    service=True,
                )},
                {"label": "Ca hai", "next": diag(
                    "Kha nang cao lien quan phan mem he thong am thanh",
                    "warning",
                    "Ca loa va mic cung bi anh huong mot luc thuong la loi phan mem/dieu khien am thanh, it khi ca hai phan cung cung hong dong thoi.",
                    [
                        "Khoi dong lai may hoan toan.",
                        "Kiem tra ban cap nhat iOS moi nhat trong Cai dat > Tong quat > Cap nhat phan mem.",
                        "Neu sau cap nhat van loi ca hai, can mang di kiem tra phan cung tong the.",
                    ],
                )},
            ],
        ),
    },

    "camera": {
        "name": "Camera (mo, khong lay net, den man hinh)",
        "category": "hardware",
        "auto_test": "camera",
        "tree": q(
            "Loi xay ra o camera truoc, camera sau, hay ca hai?",
            [
                {"label": "Ca hai", "next": diag(
                    "Nhieu kha nang la loi phan mem/ung dung Camera",
                    "warning",
                    "Ca hai camera cung loi dong thoi thuong lien quan phan mem hon la trung hop ca hai cum camera vat ly cung hong.",
                    [
                        "Dong hoan toan app Camera va mo lai.",
                        "Khoi dong lai may.",
                        "Kiem tra Cai dat > Tong quat > Cap nhat phan mem de vá loi da biet.",
                    ],
                )},
                {"label": "Chi mot camera", "next": q(
                    "Ong kinh co vet ban, tray xuoc hay dau hieu va dap khong?",
                    [
                        {"label": "Co", "next": diag(
                            "Nghi ngo hong vat ly ong kinh/cam bien",
                            "critical",
                            "Vet xuoc hoac dau hieu va dap tren cum camera co the anh huong truc tiep den chat luong lay net va hinh anh.",
                            [
                                "Lau nhe ong kinh bang khan mem, kiem tra lai truoc.",
                                "Neu van mo/den sau khi lau sach, nhieu kha nang can thay cum camera.",
                                "Mang den co so bao hanh/sua chua uy tin de kiem tra.",
                            ],
                            service=True,
                        )},
                        {"label": "Khong", "next": diag(
                            "Co the loi phan mem rieng cho mot camera",
                            "warning",
                            "Neu ong kinh sach ma van loi mot ben, kha nang la xung dot phan mem hoac loi hieu chuan camera.",
                            [
                                "Vao Cai dat > Tong quat > Cap nhat phan mem.",
                                "Thu khoi dong lai may.",
                                "Neu van con loi, can kiem tra phan cung tai co so uy tin.",
                            ],
                            service=True,
                        )},
                    ],
                )},
            ],
        ),
    },

    # ---------------- SOFTWARE ----------------

    "lag": {
        "name": "May treo / lag / cham",
        "category": "software",
        "auto_test": "storage",
        "tree": q(
            "May bi cham moi luc hay chi khi dung mot app cu the?",
            [
                {"label": "Moi luc, chung chung", "next": diag(
                    "Nghi ngo day bo nho hoac qua nhieu app/tab chay ngam",
                    "warning",
                    "May cham toan dien thuong lien quan dung luong luu tru gan day hoac qua nhieu tien trinh chay nen tich luy lau ngay.",
                    [
                        "Kiem tra Cai dat > Cai dat chung > Dung luong iPhone, xoa bot anh/video/app khong can.",
                        "Khoi dong lai may de giai phong RAM.",
                        "Neu con it hon 1-2GB trong, nen don dep them truoc khi danh gia lai.",
                    ],
                )},
                {"label": "Chi mot app cu the", "next": diag(
                    "Nhieu kha nang loi rieng cua app do, khong phai may",
                    "ok",
                    "Khi chi mot ung dung bi cham/treo, van de thuong nam o chinh app do (phien ban loi, cache hong) hon la phan cung hay he dieu hanh.",
                    [
                        "Xoa va cai lai app do.",
                        "Kiem tra cap nhat moi nhat cua app tren App Store.",
                        "Neu van loi, bao loi cho nha phat trien app do.",
                    ],
                )},
            ],
        ),
    },

    "crash": {
        "name": "App bi crash / thoat lien tuc",
        "category": "software",
        "auto_test": None,
        "tree": q(
            "Tinh trang nay xay ra voi mot app hay nhieu app khac nhau?",
            [
                {"label": "Mot app duy nhat", "next": diag(
                    "Loi cuc bo o app do",
                    "ok",
                    "App don le bi crash thuong do ban than app loi hoac chua tuong thich voi ban iOS hien tai.",
                    [
                        "Cap nhat app len phien ban moi nhat tren App Store.",
                        "Xoa va cai lai app.",
                        "Neu van crash, kiem tra app co yeu cau ban iOS moi hon khong.",
                    ],
                )},
                {"label": "Nhieu app khac nhau", "next": diag(
                    "Nghi ngo loi he dieu hanh hoac day bo nho",
                    "warning",
                    "Khi nhieu app khong lien quan cung crash, nguyen nhan thuong nam o he dieu hanh hoac tai nguyen may (bo nho, dung luong) chu khong phai tung app rieng le.",
                    [
                        "Khoi dong lai may hoan toan.",
                        "Cap nhat len ban iOS moi nhat trong Cai dat > Tong quat > Cap nhat phan mem.",
                        "Kiem tra dung luong con trong Cai dat > Cai dat chung > Dung luong iPhone.",
                    ],
                )},
            ],
        ),
    },

    "update_fail": {
        "name": "Khong cap nhat duoc iOS / loi khi update",
        "category": "software",
        "auto_test": None,
        "tree": q(
            "Loi xuat hien luc nao?",
            [
                {"label": "Khi dang tai xuong ban cap nhat", "next": diag(
                    "Nghi ngo ket noi mang hoac dung luong khong du",
                    "warning",
                    "Loi tai xuong thuong do wifi khong on dinh hoac may khong du dung luong trong de chua ban cap nhat.",
                    [
                        "Kiem tra Cai dat > Cai dat chung > Dung luong iPhone, dam bao con it nhat 5-6GB trong.",
                        "Doi sang mang wifi khac on dinh hon, tranh dung 4G/5G de cap nhat.",
                        "Thu lai qua iTunes/Finder tren may tinh neu cap nhat qua may van loi.",
                    ],
                )},
                {"label": "Khi dang cai dat / khoi dong lai", "next": diag(
                    "Nghi ngo loi trong qua trinh cai dat firmware",
                    "critical",
                    "Loi xay ra ngay giai doan cai dat co the khien may bi treo logo hoac vong lap khoi dong, can xu ly can than hon.",
                    [
                        "Khong ngat nguon hay rut sac giua chung khi dang cai dat.",
                        "Neu may bi treo qua 30-45 phut, thu ep khoi dong lai (giu Nguon + Giam am luong tuy dong may).",
                        "Neu van khong vao duoc may, can dung che do khoi phuc (Recovery Mode) qua may tinh — nen nho nguoi co kinh nghiem ho tro.",
                    ],
                    service=True,
                )},
            ],
        ),
    },

    "wifi_bt": {
        "name": "Wifi / Bluetooth khong ket noi duoc",
        "category": "software",
        "auto_test": "network",
        "tree": q(
            "Van de la voi Wifi, Bluetooth, hay ca hai?",
            [
                {"label": "Ca hai cung luc", "next": diag(
                    "Nghi ngo loi module mang chung hoac can reset cai dat mang",
                    "warning",
                    "Ca Wifi va Bluetooth cung loi mot luc thuong lien quan phan mem quan ly ket noi cua he thong.",
                    [
                        "Vao Cai dat > Tong quat > Chuyen hoac dat lai iPhone > Dat lai > Dat lai cai dat mang.",
                        "Khoi dong lai may sau khi dat lai.",
                        "Neu van loi ca hai sau buoc tren, nen mang di kiem tra phan cung anten.",
                    ],
                    service=True,
                )},
                {"label": "Chi mot trong hai", "next": diag(
                    "Kha nang loi cau hinh hoac thiet bi ket noi cu the",
                    "ok",
                    "Khi chi mot dich vu bi loi, thuong do cai dat rieng hoac xung dot voi thiet bi/mang cu the dang ket noi.",
                    [
                        "Quen mang Wifi (hoac huy ghep noi Bluetooth) roi ket noi lai tu dau.",
                        "Kiem tra thiet bi/router co dang cap nhat hoac gap loi rieng khong.",
                        "Neu chi mot mang/thiet bi cu the bi loi, van de nhieu kha nang o phia thiet bi do, khong phai iPhone.",
                    ],
                )},
            ],
        ),
    },

    # ---------------- "VIRUS" / MA DOC ----------------

    "malware": {
        "name": "Nghi ngo dinh virus / ma doc",
        "category": "software",
        "auto_test": None,
        "tree": q(
            "Dau hieu cu the la gi?",
            [
                {"label": "Quang cao/popup tu bat lien tuc trong Safari", "next": diag(
                    "Nhieu kha nang do trang web hoac tien ich mo rong doc hai, khong phai virus he thong",
                    "warning",
                    "iPhone khong the bi 'nhiem virus' kieu file thuc thi nhu may tinh, nhung popup/quang cao lien tuc thuong do trang web doc hai, tien ich Safari la, hoac cau hinh (profile) khong ro nguon goc.",
                    [
                        "Vao Cai dat > Safari > Xoa Lich su va Du lieu Trang web.",
                        "Vao Cai dat > Safari > Tien ich mo rong, tat/go bat ky tien ich la nao.",
                        "Vao Cai dat > Cai dat chung > VPN & Quan ly thiet bi, xoa bat ky ho so cau hinh (profile) la nao khong phai do cong ty/truong hoc cua ban cai.",
                        "Tranh nhan vao quang cao dang 'canh bao virus' — day thuong la chinh chieu tro lua dao.",
                    ],
                )},
                {"label": "May tu dong cai app la / hanh vi bat thuong", "next": diag(
                    "Nghi ngo profile cau hinh hoac tai khoan Apple ID bi anh huong",
                    "critical",
                    "App tu xuat hien ma ban khong cai, hoac cai dat tu doi thay doi, la dau hieu can kiem tra ngay ca profile quan ly thiet bi lan bao mat Apple ID, khong chi don gian la xoa app.",
                    [
                        "Vao Cai dat > Cai dat chung > VPN & Quan ly thiet bi, kiem tra va xoa profile la.",
                        "Doi mat khau Apple ID ngay va bat Xac thuc hai yeu to (2FA) neu chua bat.",
                        "Kiem tra Cai dat > Ten cua ban > tab Thiet bi, dang xuat cac thiet bi la khong nhan ra.",
                        "Neu van tiep tuc sau cac buoc tren, nen mang may den Apple Store/co so uy tin de kiem tra sau.",
                    ],
                    service=True,
                )},
                {"label": "Nhan tin canh bao 'may bi nhiem virus' tu mot trang web", "next": diag(
                    "Gan nhu chac chan la lua dao (scareware), khong phai virus that",
                    "ok",
                    "Cac thong bao 'iPhone cua ban da bi nhiem virus, nhan de quet ngay' hien tren trinh duyet gan nhu luon la chieu lua de ban tai app gia hoac nhap thong tin ca nhan. iOS khong the tu quet virus theo kieu do.",
                    [
                        "Dong tab Safari do ngay, khong nhan bat ky nut nao trong thong bao.",
                        "Khong tai bat ky app 'diet virus' nao duoc quang cao qua popup nhu vay.",
                        "Xoa lich su/du lieu trang web trong Cai dat > Safari de tranh popup lap lai.",
                    ],
                )},
            ],
        ),
    },
}


def categories_summary():
    """Tra ve danh sach problem groupby category, dung cho trang chon."""
    out = {"hardware": [], "software": []}
    for pid, p in PROBLEMS.items():
        out[p["category"]].append({
            "id": pid,
            "name": p["name"],
            "auto_test": p["auto_test"],
        })
    return out
