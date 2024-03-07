from datetime import date
from django.test import TestCase
from parse_m2.models import Metro2Event, M2DataFile, AccountHolder, AccountActivity
from rest_framework.renderers import JSONRenderer
from parse_m2.serializers import AccountActivitySerializer

class AccountActivitySerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an AccountActivity record
        event = Metro2Event(name="tst")
        event.save()
        file = M2DataFile(event=event, file_name="tst.txt")
        file.save()
        acct_holder = AccountHolder(
            data_file=file,activity_date=date(2023, 11, 30), cons_acct_num="98765")
        acct_holder.save()
        self.acct_activity = AccountActivity(
            account_holder=acct_holder,
            activity_date=date(2023,11,20),
            cons_acct_num="98765",
            port_type="port_type",
            acct_type="acct_type",
            date_open=date(2020,3,17),
            credit_limit=9000,
            hcola=90210,
            terms_dur="terms_dur",
            terms_freq="terms_freq",
            smpa=5,
            actual_pmt_amt=201,
            acct_stat="acct_stat",
            pmt_rating="pmt_rating",
            php="php",
            spc_com_cd="spc_com_cd",
            compl_cond_cd="compl_cond_cd",
            current_bal=12345,
            amt_past_due=111,
            orig_chg_off_amt=0,
            doai=date(2023,11,3),
            dofd=None,
            date_closed=None,
            dolp=date(2023,1,1),
            int_type_ind="int_type_ind",
        )
        self.acct_activity.save()

        self.json_representation = {
            "id": self.acct_activity.id,
            "activity_date": "2023-11-20",
            "port_type": "port_type",
            "acct_type": "acct_type",
            "date_open": "2020-03-17",
            "credit_limit": 9000,
            "hcola": 90210,
            "terms_dur": "terms_dur",
            "terms_freq": "terms_freq",
            "smpa": 5,
            "actual_pmt_amt": 201,
            "acct_stat": "acct_stat",
            "pmt_rating": "pmt_rating",
            "php": "php",
            "spc_com_cd": "spc_com_cd",
            "compl_cond_cd": "compl_cond_cd",
            "current_bal": 12345,
            "amt_past_due": 111,
            "orig_chg_off_amt": 0,
            "doai": "2023-11-03",
            "dofd": None,
            "date_closed": None,
            "dolp": "2023-01-01",
            "int_type_ind": "int_type_ind",
        }

    def test_account_activity_serializer(self):
        serializer = AccountActivitySerializer(self.acct_activity)
        self.assertEqual(serializer.data, self.json_representation)

    def test_account_activity_serializer_many_true(self):
        activity_records = [self.acct_activity]
        serializer = AccountActivitySerializer(activity_records, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)
