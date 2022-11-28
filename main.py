import fitz
import os

# File Parameters
fname = "1.pdf"
in_dir = "res/"
out_dir = "out/"

# Clear out dir
for file_name in os.listdir(out_dir):
    # construct full file path
    file = out_dir + file_name
    if os.path.isfile(file):
        print('Deleting file:', file)
        os.remove(file)


# Each input file
for file_name in os.listdir(in_dir):
    in_path = in_dir + file_name
    out_path = out_dir + file_name
    if os.path.isfile(in_path):
        print("Redacting " + file_name)
        doc = fitz.open(in_path)

        # Test
        number_of_pages = len(doc)
        t_pages = number_of_pages - 1

        # Text page
        maxis_page  = -1
        maxis_r = (0, 0, 0 ,0)

        for pn in range(number_of_pages):
            pp = doc[pn]
            tp = pp.get_textpage()
            search_r = tp.search("MAXIS", quads=False)
            if len(search_r) >= 1:
                maxis_page = pn
                maxis_r = search_r.pop()

        # Constants
        table_x0 = 23.5
        table_x1 = 587
        table_y1 = 846

        # Instantiate list
        areas = list()

        # Address
        addr_x0 = table_x0
        addr_x1 = 156
        addr_y0 = 103
        addr_y1 = 135
        areas.append((addr_x0, addr_y0, addr_x1, addr_y1))

        # Acc num
        acc_x0 = table_x0
        acc_l = 114.2
        acc_r = 167.5
        acc_x1 = table_x1
        acc_y0 = 227.5
        acc_y1 = 237.5
        areas.append((acc_x0, acc_y0, acc_l, acc_y1))
        areas.append((acc_r, acc_y0, acc_x1, acc_y1))

        # Transactions P0
        t_x0 = table_x0
        t_x1 = table_x1
        t_y0 = 494.1
        t_y1 = table_y1
        if (maxis_page != 0):
            areas.append((t_x0, t_y0, t_x1, t_y1))
        else:
            print("MAXIS IN PAGE 0!!!!")

        # Draw page 0
        page = doc[0]

        for r in areas:
            page.add_redact_annot(r, fill=(0, 0, 0))
        
        page.apply_redactions()

        # Transaction Px
        tx_x0 = table_x0
        tx_y0 = 120
        tx_x1 = table_x1
        tx_y1 = table_y1

        for tpn in range(1, t_pages):
            areas.clear()
            page = doc[tpn]
            if maxis_page == tpn:
                maxis_y_up = maxis_r.y0
                maxis_y_down = maxis_r.y1
                areas.append((tx_x0, tx_y0, tx_x1, maxis_y_up))
                areas.append((tx_x0, maxis_y_down, tx_x1, tx_y1))
            else:
                areas.append((tx_x0, tx_y0, tx_x1, tx_y1))
                
            for r in areas:
                page.add_redact_annot(r, fill=(0, 0, 0))
            
            page.apply_redactions()

        # Delete last page
        doc.delete_page(number_of_pages-1)

        doc.save(out_path)