from make_api_test_requests import *


run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/', 'h': {}, 'b': '',
    'e': 'Active', })
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/ck/asdfslkj', 'h': {}, 'b': '',
    'e': 'False', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/ck/alkryukov', 'h': {}, 'b': '',
    'e': 'True', }),

run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/user',
    'h': { "Authorization": "Bearer mac" },
    'b': { "nick": "alkryukov", "passwd": "pp" },
    'e': 'deleted', })
run_test( { 
    'm': 'post',    'u': 'http://localhost:8100/user',
    'h': {},
    'b': { "nick": "alkryukov", "passwd": "pp", "settings": "", "device_info": "mac" },
    'e': 'device_id', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/user',
    'h': {"Authorization": "Bearer mac"},
    'b': { "new_settings": "new_sets", "cur_passwd": "kkkk", "new_passwd": "kkkk" },
    'e': 'updated', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/user/alkryukov',
    'h': { "Authorization": "Bearer mac" },
    'b': {  },
    'e': 'alkryukov', }),
run_test( { 
    'm': 'options', 'u': 'http://localhost:8100/user',
    'h': {  },
    'b': {  },
    'e': 'Method Not Allowed', }),

run_test( { 
    'm': 'post',    'u': 'http://localhost:8100/device',
    'h': {  },
    'b': { 'nick': 'alkryukov', 'passwd': 'pp', 'device_info': 'newdevice' }, 
    'e': 'device_id', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/devices',
    'h': { "Authorization": "Bearer mac" },
    'b': '',
    'e': 'devices', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/device/99',
    'h': { "Authorization": "Bearer kkriukov" },
    'b': { 'device_info': 'newdeviceinfo' },
    'e': 'device_info', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/device/99',
    'h': { "Authorization": "Bearer mac" },
    'b': {  },
    'e': 'permission denied', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/device/',
    'h': { "Authorization": "Bearer newdevice" },
    'b': {  },
    'e': 'deleted', }),

run_test( {
    'test_id': 'post_proj_al',
    'm': 'post',    'u': 'http://localhost:8100/project',
    'h': { "Authorization": "Bearer mac" },
    'b': { "title": "akproj", "settings": "", "p_status": "active" }, 
    'e': 'user_role', }),
run_test( {
    'test_id': 'post_proj_al2',
    'm': 'post',    'u': 'http://localhost:8100/project',
    'h': { "Authorization": "Bearer mac" },
    'b': { "title": "akproj2", "settings": "", "p_status": "active" }, 
    'e': 'user_role', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/project',
    'h': {  },
    'b': {  }, 
    'e': 'Method Not Allowed', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/project/17',
    'h': { "Authorization": "Bearer kkriukov" },
    'b': { "title": "put title", "settings": '', "p_status": "active" },
    'e': 'proj_title', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/project/17',
    'h': { "Authorization": "Bearer mac" },
    'b': {  },
    'e': 'permission denied', }),

run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/userprojects',
    'h': { "Authorization": "Bearer mac" },
    'b': {  }, 
    'e': 'user_role', }),
run_test( { 
    'm': 'post',     'u': 'http://localhost:8100/userproject',
    'h': { "Authorization": "Bearer kkriukov" },
    'b': { "proj_id": 17, "nick": "alkryukov", "user_role": "member" },
    'e': 'user_role', }),
run_test( { 
    'm': 'put',    'u': 'http://localhost:8100/userproject',
    'h': {  },
    'b': {  }, 
    'e': 'Method Not Allowed', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/userproject',
    'h': { "Authorization": "Bearer kkriukov" },
    'b': { "proj_id": 17, "nick": "alkryukov" },
    'e': 'deleted', }),

run_test( { 
    'test_id': 'post_label_al',
    'm': 'post',    'u': 'http://localhost:8100/label',
    'h': { "Authorization": "Bearer mac" },
    'b': { 'title': 'my_label', 'proj_id': artif['post_proj_al2']['id']  }, 
    'e': 'title', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/label/' + str(artif['post_label_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': { 'new_title': 'my_new_label' },
    'e': 'chagned', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/labels/' + str(artif['post_proj_al2']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': {  }, 
    'e': 'labels', }),
run_test( { 
    'm': 'post',    'u': 'http://localhost:8100/labels/1', 'h': {}, 'b': {}, 
    'e': 'Method Not Allowed', }),
run_test( { 
    'm': 'get',    'u': 'http://localhost:8100/label', 'h': {}, 'b': {}, 
    'e': 'Method Not Allowed', }),

run_test( { 
    'm': 'post',    'u': 'http://localhost:8100/wallet',
    'h': { "Authorization": "Bearer mac" }, 
    'b': { 'title': "k_wallet", 'properties': "", 'proj_id': 17 }, 
    'e': 'permission denied', }),
run_test( {
    'test_id': 'post_wlt_al',
    'm': 'post',    'u': 'http://localhost:8100/wallet',
    'h': { "Authorization": "Bearer mac" }, 
    'b': { 'title': "al_wallet", 'properties': "", 'proj_id': artif['post_proj_al2']['id'] }, 
    'e': 'id', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/wallet/' + str(artif['post_wlt_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': { 'title': "upd_al_wallet", 'properties': "", },
    'e': 'upd_al_wallet', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/portfolio/' + str(artif['post_wlt_al']['pf_id']),
    'h': { "Authorization": "Bearer mac" },
    'b': { 'pf_title': "al_upd_portfolio", 'pf_properties': "", },
    'e': 'al_upd_portfolio', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/wallets/' + str(artif['post_proj_al2']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': {  }, 
    'e': 'wallets', }),
run_test( { 
    'm': 'options', 'u': 'http://localhost:8100/wallet', 'h': {}, 'b': {},
    'e': 'Method Not Allowed', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/portfolio/1',
    'h': { "Authorization": "Bearer mac" },
    'b': {  }, 
    'e': 'Method Not Allowed', }),

run_test( { 
    'm': 'post',    'u': 'http://localhost:8100/transaction',
    'h': {  },
    'b': {  }, 
    'e': 'Not authenticated', }),
run_test( { 
    'test_id': 'post_tr_a_al',
    'm': 'post',    'u': 'http://localhost:8100/transaction',
    'h': { "Authorization": "Bearer mac" },
    'b': { 'date': "2023-03-03 23:00:00", 'value': 400, 'comment': 'my comment', 'to_wallet_id': artif['post_wlt_al']['id'] }, 
    'e': 'to_wallet_id', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/transaction/' + str(artif['post_tr_a_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': { 'date': "2023-03-03 23:10:00", 'comment': 'my updated comment' },
    'e': 'my updated comment', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/transactions/' + str(artif['post_wlt_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': '', 
    'e': 'transactions', }),
run_test( { 
    'm': 'options', 'u': 'http://localhost:8100/transaction', 'h': {}, 'b': {},
    'e': 'Method Not Allowed', }),
run_test( {
    'm': 'post',    'u': 'http://localhost:8100/transactionlabel',
    'h': { "Authorization": "Bearer mac" },
    'b': { 'label_id': artif['post_label_al']['id'], 'transaction_id': artif['post_tr_a_al']['id'] }, 
    'e': 'changed', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/transactionlabels/' + str(artif['post_proj_al2']['id']), 
    'h': { "Authorization": "Bearer mac" },
    'b': {  },
    'e': 'transaction_labels', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/transactionlabel', 'h': {}, 'b': {},
    'e': 'Method Not Allowed', }),
run_test( { 
    'm': 'post',    'u': 'http://localhost:8100/transactionlabels/1', 'h': {}, 'b': {},
    'e': 'Method Not Allowed', }),
run_test( { 
    'test_id': 'post_sc_a_al',
    'm': 'post',    'u': 'http://localhost:8100/schedule',
    'h': { "Authorization": "Bearer mac" },
    'b': { 'comment': 'my schedule', 'date': "2023-03-07", 'tz_offset_min': 60, 'repeat': 'monthly', 'value': 20, 'percent': 1, 'from_wallet_id': artif['post_wlt_al']['id'] }, 
    'e': 'my schedule', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/schedule/' + str(artif['post_sc_a_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': { 'comment': 'my upd schedule', 'date': "2023-03-09", 'tz_offset_min': 60, 'repeat': 'monthly', 'value': 22, 'percent': 1 },
    'e': 'my upd schedule', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/schedules/' + str(artif['post_proj_al2']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': '', 
    'e': 'schedules', }),
run_test( { 
    'm': 'post',    'u': 'http://localhost:8100/schedules/1', 'h': {}, 'b': {}, 
    'e': 'Method Not Allowed', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/schedule', 'h': {}, 'b': {},
    'e': 'Method Not Allowed', }),
run_test( {
    'm': 'post',    'u': 'http://localhost:8100/schedulelabel',
    'h': { "Authorization": "Bearer mac" },
    'b': { 'label_id': artif['post_label_al']['id'], 'schedule_id': artif['post_sc_a_al']['id'] }, 
    'e': 'changed', }),
run_test( { 
    'm': 'get',     'u': 'http://localhost:8100/schedulelabels/' + str(artif['post_proj_al2']['id']), 
    'h': { "Authorization": "Bearer mac" },
    'b': {  },
    'e': 'schedule_labels', }),
run_test( { 
    'm': 'put',     'u': 'http://localhost:8100/schedulelabel', 'h': {}, 'b': {},
    'e': 'Method Not Allowed', }),
run_test( { 
    'm': 'post',    'u': 'http://localhost:8100/schedulelabels/1', 'h': {}, 'b': {},
    'e': 'Method Not Allowed', }),



run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/schedulelabel',
    'h': { "Authorization": "Bearer mac" },
    'b': { 'label_id': artif['post_label_al']['id'], 'schedule_id': artif['post_sc_a_al']['id'] },
    'e': 'deleted', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/schedule/' + str(artif['post_sc_a_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': {},
    'e': 'deleted', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/transactionlabel',
    'h': { "Authorization": "Bearer mac" },
    'b': { 'label_id': artif['post_label_al']['id'], 'transaction_id': artif['post_tr_a_al']['id'] },
    'e': 'deleted', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/transaction/' + str(artif['post_tr_a_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': {},
    'e': 'rollback', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/label/' + str(artif['post_label_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': {  },
    'e': 'deleted', }),
run_test( { 
    'm': 'delete',  'u': 'http://localhost:8100/wallet/' + str(artif['post_wlt_al']['id']),
    'h': { "Authorization": "Bearer mac" },
    'b': {  },
    'e': 'deleted', }),


summary()

