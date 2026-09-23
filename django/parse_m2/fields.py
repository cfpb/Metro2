# field dictionaries
# The start and end positions for each field match those in the CRRG.

header_fields = {
    "rdw_header":(1, 4),
    "record_identifier_header":(5, 10),
    "cycle_identifier_header":(11, 12),
    "innovis_program_identifier":(13, 22),
    "equifax_program_identifier":(23, 32),
    "experian_program_identifier":(33, 37),
    "transunion_program_identifier":(38, 47),
    # Temporary: updated for this event
    "activity_date":(43, 51, "date"),
    "date_created":(56, 63),
    "program_date":(64, 71),
    "program_revision_date":(72, 79),
    "reporter_name":(80, 119),
    "reporter_address":(120, 215),
    "reporter_telephone_number":(216, 225),
    "software_vendor_name":(226, 265),
    "software_version_number":(266, 270),
    "microbilt_prbc_program_identifier":(271, 280),
    "reserved_header":(281, 426)
}

# Temporary: updated for this event
base_fields = {
    # 1. Removed fields we don't save on the model
    # 2. Updated start and end indices for each field
    #    to match event file format
    "id_num":(21, 40),
    "cons_acct_num":(50, 79),
    "port_type":(80, 80),
    "acct_type":(81, 82),
    "date_open":(83, 92, "date"),
    "credit_limit":(93, 102, "numeric"),
    "hcola":(103, 112, "numeric"),
    "terms_dur":(113, 115),
    "terms_freq":(116, 116),
    "smpa":(117, 126, "numeric"),
    "actual_pmt_amt":(127, 136, "numeric"),
    "acct_stat":(137, 138),
    "pmt_rating":(139, 139),
    "php":(140, 163),
    "spc_com_cd":(164, 165),
    "compl_cond_cd":(166, 167),
    "current_bal":(168, 177, "numeric"),
    "amt_past_due":(178, 187, "numeric"),
    "orig_chg_off_amt":(188, 197, "numeric"),
    "doai":(198, 207, "date"),
    "dofd":(208, 217, "date optional"),
    "date_closed":(218, 227, "date optional"),
    "dolp":(228, 237, "date optional"),
    "int_type_ind":(255, 255),
    "surname":(256, 280),
    "first_name":(281, 300),
    "middle_name":(301, 320),
    "gen_code":(321, 321),
    "ssn":(322, 331),
    "dob":(332, 341),
    "phone_num":(342, 352),
    "ecoa":(353, 353),
    "cons_info_ind":(354, 355),
    "country_cd":(356, 357),
    "addr_line_1":(358, 389),
    "addr_line_2":(390, 421),
    "city":(422, 441),
    "state":(442, 443),
    "zip":(444, 452),
    "addr_ind":(453, 453),
    "res_cd":(454, 454),
}

j1_fields = {
    "segment_identifier_j1":(1, 2),
    "reserved_j1":(3, 3),
    "surname_j1":(4, 28),
    "first_name_j1":(29, 48),
    "middle_name_j1":(49, 68),
    "gen_code_j1":(69, 69),
    "ssn_j1":(70, 78),
    "dob_j1":(79, 86),
    "phone_num_j1":(87, 96),
    "ecoa_j1":(97, 97),
    "cons_info_ind_j1":(98, 99),
    "reserved_j1_2":(100, 100),
}

j2_fields = {
    "segment_identifier_j2":(1, 2),
    "reserved_j2":(3, 3),
    "surname_j2":(4, 28),
    "first_name_j2":(29, 48),
    "middle_name_j2":(49, 68),
    "gen_code_j2":(69, 69),
    "ssn_j2":(70, 78),
    "dob_j2":(79, 86),
    "phone_num_j2":(87, 96),
    "ecoa_j2":(97, 97),
    "cons_info_ind_j2":(98, 99),
    "country_cd_j2":(100, 101),
    "addr_line_1_j2":(102, 133),
    "addr_line_2_j2":(134, 165),
    "city_j2":(166, 185),
    "state_j2":(186, 187),
    "zip_j2":(188, 196),
    "addr_ind_j2":(197, 197),
    "res_cd_j2":(198, 198),
    "reserved_j2_2":(199, 200),
}

k1_fields = {
    "k1_seg_id":(1, 2),
    "k1_orig_creditor_name":(3, 32),
    "k1_creditor_classification":(33, 34),
}

k2_fields = {
    "k2_seg_id":(1, 2),
    "k2_purch_sold_ind":(3, 3),
    "k2_purch_sold_name":(4, 33),
    "reserved_k2":(34, 34),
}

k3_fields = {
    "k3_seg_id":(1, 2),
    "k3_agcy_id":(3, 4),
    "k3_agcy_acct_num":(5, 22),
    "k3_min":(23, 40),
}

k4_fields = {
    "k4_seg_id":(1, 2),
    "k4_spc_pmt_ind":(3, 4),
    "k4_deferred_pmt_st_dt":(5, 12, "date optional"),
    "k4_balloon_pmt_due_dt":(13, 20, "date optional"),
    "k4_balloon_pmt_amt":(21, 29, "numeric optional"),
    "reserved_k4":(30, 30),
}

l1_fields = {
    "l1_seg_id":(1, 2),
    "l1_change_ind":(3, 3),
    "l1_new_acc_num":(4, 33),
    "l1_new_id_num":(34, 53),
    "reserved_l1":(54, 54),
}

n1_fields = {
    "n1_seg_id":(1, 2),
    "n1_employer_name":(3, 32),
    "employer_addr1":(33, 64),
    "employer_addr2":(65, 96),
    "employer_city":(97, 116),
    "employer_state":(117, 118),
    "employer_zip":(119, 127),
    "occupation":(128, 145),
    "reserved_n1":(146, 146),
}

# combine field dictionaries into 1
fields = {
    "header": header_fields,
    "base": base_fields,
    "j1": j1_fields,
    "j2": j2_fields,
    "k1": k1_fields,
    "k2": k2_fields,
    "k3": k3_fields,
    "k4": k4_fields,
    "l1": l1_fields,
    "n1": n1_fields,
}

# length of each segment
seg_length = {
    "header": 426,
    # Temporary: updated for this event
    "base": 454,
    "j1": 100,
    "j2": 200,
    "k1": 34,
    "k2": 34,
    "k3": 40,
    "k4": 30,
    "l1": 54,
    "n1": 146,
    "trailer": 426
}
