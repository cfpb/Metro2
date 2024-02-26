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
    "activity_date":(48, 55, "date"),
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

base_fields = {
    "rdw":(1, 4),
    "proc_ind":(5, 5),
    "time_stamp":(6, 13),
    "throw_out_hms":(14, 19),
    "reserved_base":(20, 20),
    "id_num":(21, 40),
    "cycle_id":(41, 42),
    "cons_acct_num":(43, 72),
    "port_type":(73, 73),
    "acct_type":(74, 75),
    "date_open":(76, 83, "date"),
    "credit_limit":(84, 92, "numeric"),
    "hcola":(93, 101, "numeric"),
    "terms_dur":(102, 104),
    "terms_freq":(105, 105),
    "smpa":(106, 114, "numeric"),
    "actual_pmt_amt":(115, 123, "numeric"),
    "acct_stat":(124, 125),
    "pmt_rating":(126, 126),
    "php":(127, 150),
    "spc_com_cd":(151, 152),
    "compl_cond_cd":(153, 154),
    "current_bal":(155, 163, "numeric"),
    "amt_past_due":(164, 172, "numeric"),
    "orig_chg_off_amt":(173, 181, "numeric"),
    "doai":(182, 189, "date"),
    "dofd":(190, 197, "date optional"),
    "date_closed":(198, 205, "date optional"),
    "dolp":(206, 213, "date optional"),
    "int_type_ind":(214, 214),
    "reserved_base_2":(215, 231),
    "surname":(232, 256),
    "first_name":(257, 276),
    "middle_name":(277, 296),
    "gen_code":(297, 297),
    "ssn":(298, 306),
    "dob":(307, 314),
    "phone_num":(315, 324),
    "ecoa":(325, 325),
    "cons_info_ind":(326, 327),
    "country_cd":(328, 329),
    "addr_line_1":(330, 361),
    "addr_line_2":(362, 393),
    "city":(394, 413),
    "state":(414, 415),
    "zip":(416, 424),
    "addr_ind":(425, 425),
    "res_cd":(426, 426),
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
    "base": 426,
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
