"""
The stats module maps statistical category identifiers from NFL.com's
GameCenter JSON feed to a representation of what we believe that statistical
category means. This mapping has been reverse engineered with a lot of help
from reddit users rasherdk and curien.

If you think anything here is wrong (or can figure out some of the unknowns),
please let me know by filing an issue here:
https://github.com/BurntSushi/nflgame/issues

For each statistical category identifier, we create a dict of 6 fields
describing that statistical category. The fields are cat, field, yds, super,
value and desc.

cat specifies which statistical category the particular stat belong in. Only
statistical categories in nflgame.player.categories should be used.

field specifies the actual statistical field corresponding to the stat. This
will manifest itself as a property on statistical objects via the API.

yds specifies a field that contains the yardage totals relevant to the stat.
If a stat does not specify yards, this field should be blank (an empty string).

super specifies parent statistical fields that must be derived (either
partially or in full) from the stat. For example, the kicking_cnt field
has no corresponding statistical category id, but it can be derived through
multiple other fields (kicking_outendzone_fielded, kicking_inendzone_fielded,
and kicking_touchback). Thus, in each of the child fields, kicking_cnt should
be listed as a parent field. Parent fields always correspond to the sum of
all their child fields.

value specifies how much each statistic is worth. This is 1 in every case
except for split sacks.

desc specifies a human readable description for the statistic. It should be
concise and clear. If a statistical category is unknown, then desc should
contain a string like 'Unknown (reason for confusion)'. Valid reasons for
confusion include "data is inconsistent" or "this looks like a duplicate" all
the way to "I have no fucking clue."
"""

categories = {
    2: {
        'cat': 'punting',
        'field': 'punting_blk',
        'yds': '',
        'super': ['punting_cnt'],
        'value': 1,
        'desc': 'Punt blocked',
    },
    3: {
        'cat': 'team',
        'field': 'rushing_first_down',
        'yds': '',
        'super': ['first_down'],
        'value': 1,
        'desc': 'First down (rush)',
    },
    4: {
        'cat': 'team',
        'field': 'passing_first_down',
        'yds': '',
        'super': ['first_down'],
        'value': 1,
        'desc': 'First down (pass)',
    },
    5: {
        'cat': 'team',
        'field': 'penalty_first_down',
        'yds': '',
        'super': ['first_down'],
        'value': 1,
        'desc': 'First down (penalty)',
    },
    6: {
        'cat': 'team',
        'field': 'third_down_conv',
        'yds': '',
        'super': ['third_down_att'],
        'value': 1,
        'desc': 'Third down conversion',
    },
    7: {
        'cat': 'team',
        'field': 'third_down_failed',
        'yds': '',
        'super': ['third_down_att'],
        'value': 1,
        'desc': 'Third down failed',
    },
    8: {
        'cat': 'team',
        'field': 'fourth_down_conv',
        'yds': '',
        'super': ['fourth_down_att'],
        'value': 1,
        'desc': 'Fourth down conversion',
    },
    9: {
        'cat': 'team',
        'field': 'fourth_down_failed',
        'yds': '',
        'super': ['fourth_down_att'],
        'value': 0,
        'desc': 'Fourth down failed',
    },
    10: {
        'cat': 'rushing',
        'field': 'rushing_att',
        'yds': 'rushing_yds',
        'super': [],
        'value': 1,
        'desc': 'Rush',
    },
    11: {
        'cat': 'rushing',
        'field': 'rushing_tds',
        'yds': 'rushing_yds',
        'super': ['rushing_att'],
        'value': 1,
        'desc': 'Rush TD',
    },
    12: {
        'cat': 'passing',
        'field': None,
        'yds': '',
        'super': [],
        'value': 0,
        'desc': 'Unknown (no clue)',
    },
    14: {
        'cat': 'passing',
        'field': 'passing_incmp',
        'yds': '',
        'super': ['passing_att'],
        'value': 1,
        'desc': 'Incomplete pass',
    },
    15: {
        'cat': 'passing',
        'field': 'passing_cmp',
        'yds': 'passing_yds',
        'super': ['passing_att'],
        'value': 1,
        'desc': 'Completed pass (total yards)',
    },
    16: {
        'cat': 'passing',
        'field': 'passing_tds',
        'yds': 'passing_yds',
        'super': ['passing_att', 'passing_cmp'],
        'value': 1,
        'desc': 'Touchdown pass (total yards)',
    },
    19: {
        'cat': 'passing',
        'field': 'passing_int',
        'yds': '',
        'super': ['passing_att', 'passing_incmp'],
        'value': 1,
        'desc': 'QB throws interception',
    },
    20: {
        'cat': 'passing',
        'field': 'passing_sk',
        'yds': 'passing_sk_yds',
        'super': [],
        'value': 1,
        'desc': 'QB sacked',
    },
    21: {
        'cat': 'receiving',
        'field': 'receiving_rec',
        'yds': 'receiving_yds',
        'super': [],
        'value': 1,
        'desc': 'Completed reception (total yards)',
    },
    22: {
        'cat': 'receiving',
        'field': 'receiving_tds',
        'yds': 'receiving_yds',
        'super': ['receiving_rec'],
        'value': 1,
        'desc': 'Touchdown reception (total yards)',
    },
    23: {
        'cat': 'lateral',
        'field': 'lateral_rec',
        'yds': 'lateral_rec_yds',
        'super': [],
        'value': 1,
        'desc': 'Lateral catch on offense',
    },
    24: {
        # This is a guess.
        'cat': 'lateral',
        'field': 'lateral_rec_tds',
        'yds': 'lateral_rec_yds',
        'super': ['lateral_rec'],
        'value': 1,
        'desc': 'Lateral catch on offense for touchdown',
    },
    25: {
        'cat': 'defense',
        'field': 'defense_int',
        'yds': 'defense_int_yds',
        'super': [],
        'value': 1,
        'desc': 'Interception',
    },
    26: {
        'cat': 'defense',
        'field': 'defense_int_tds',
        'yds': 'defense_int_yds',
        'super': ['defense_int'],
        'value': 1,
        'desc': 'Interception returned for touchdown',
    },
    27: {
        'cat': 'lateral',
        'field': 'lateral_int_rec',
        'yds': 'lateral_int_rec_yds',
        'super': [],
        'value': 1,
        'desc': 'Lateral catch after interception',
    },
    28: {
        'cat': 'lateral',
        'field': 'lateral_int_rec_tds',
        'yds': 'lateral_int_rec_yds',
        'super': ['lateral_int_rec'],
        'value': 1,
        'desc': 'Lateral catch after interception for touchdown',
    },
    29: {
        'cat': 'punting',
        'field': 'punting_cnt',
        'yds': 'punting_yds',
        'super': [],
        'value': 1,
        'desc': 'Punt',
    },
    30: {
        'cat': 'punting',
        'field': 'punting_i20',
        'yds': '',
        'super': ['punting_cnt'],
        'value': 1,
        'desc': 'Punt inside 20',
    },
    31: {
        'cat': 'punting',
        'field': None,
        'yds': '',
        'super': [],
        'value': 0,
        'desc': 'Unknown (inside 20 return? only happened 4 times in 2011)',
    },
    32: {
        'cat': 'punting',
        'field': 'punting_touchback',
        'yds': 'punting_yds',
        'super': ['punting_cnt'],
        'value': 1,
        'desc': 'Punt (touchback)',
    },
    33: {
        'cat': 'puntret',
        'field': 'puntret_tot',
        'yds': 'puntret_yds',
        'super': [],
        'value': 1,
        'desc': 'Punt return',
    },
    34: {
        'cat': 'puntret',
        'field': 'puntret_tds',
        'yds': 'puntret_yds',
        'super': [],
        'value': 1,
        'desc': 'Punt return touchdown',
    },
    35: {
        'cat': 'lateral',
        'field': 'lateral_punt_rec',
        'yds': 'lateral_punt_rec_yds',
        'super': [],
        'value': 1,
        'desc': 'Lateral catch after punt',
    },
    36: {
        # This is a guess.
        'cat': 'lateral',
        'field': 'lateral_punt_rec_tds',
        'yds': 'lateral_punt_rec_yds',
        'super': ['lateral_punt_rec'],
        'value': 1,
        'desc': 'Lateral catch after punt for touchdown',
    },
    37: {
        'cat': 'team',
        'field': 'puntret_oob',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Punt out of bounds (receiving team)',
    },
    38: {
        'cat': 'team',
        'field': 'puntret_downed',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Punt downed by kicking team',
    },
    39: {
        'cat': 'puntret',
        'field': 'puntret_fair',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Punt fair catch',
    },
    40: {
        'cat': 'team',
        'field': 'puntret_touchback',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Punt return touchback',
    },
    41: {
        'cat': 'kicking',
        'field': 'kicking_outendzone_fielded',
        'yds': 'kicking_yds',
        'super': ['kicking_cnt', 'kicking_fielded'],
        'value': 1,
        'desc': 'Kickoff fielded from outside the endzone',
    },
    42: {
        'cat': 'kicking',
        'field': None,
        'yds': '',
        'super': [],
        'value': 0,
        'desc': 'Unknown (kick fielded? redundant?)',
    },
    43: {
        'cat': 'kicking',
        'field': 'kicking_inendzone_fielded',
        'yds': 'kicking_yds',
        'super': ['kicking_cnt', 'kicking_fielded'],
        'value': 1,
        'desc': 'Kickoff fielded from inside the endzone',
    },
    44: {
        'cat': 'kicking',
        'field': 'kicking_touchback',
        'yds': 'kicking_yds',
        'super': ['kicking_cnt', 'kicking_tbacks'],
        'value': 1,
        'desc': 'Kickoff touchback',
    },
    45: {
        'cat': 'kickret',
        'field': 'kickret_ret',
        'yds': 'kickret_yds',
        'super': [],
        'value': 1,
        'desc': 'Kickoff return',
    },
    46: {
        'cat': 'kickret',
        'field': 'kickret_td',
        'yds': 'kickret_yds',
        'super': ['kickret_ret'],
        'value': 1,
        'desc': 'Kickoff return TD',
    },
    47: {
        'cat': 'lateral',
        'field': None,
        'yds': '',
        'value': 0,
        'desc': 'Unknown (lateral after kickoff; name is inconsistent?)',
    },
    48: {
        'cat': 'lateral',
        'field': None,
        'yds': '',
        'value': 0,
        'desc': 'Unknown (lateral after kickoff for td?)',
    },
    49: {
        'cat': 'team',
        'field': 'kickret_oob',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Kickoff return out of bounds',
    },
    50: {
        'cat': 'kickret',
        'field': 'kickret_fair',
        'yds': '',
        'super': ['kickret_ret'],
        'value': 1,
        'desc': 'Kickoff return (fair catch)',
    },
    51: {
        'cat': 'team',
        'field': 'kickret_touchback_outendzone',
        'yds': '',
        'super': [],
        'value': 0,
        'desc': 'Kick return touchback out of endzone',
    },
    52: {
        'cat': 'fumbles',
        'field': 'fumbles_strp',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Fumbled (stripped)',
    },
    53: {
        'cat': 'fumbles',
        'field': 'fumbles_drop',
        'yds': '',
        'super': ['fumbles_tot'],
        'value': 1,
        'desc': 'Fumbled (drop)',
    },
    54: {
        'cat': 'fumbles',
        'field': 'fumbles_oob',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Fumbled (oob)',
    },
    55: {
        'cat': 'fumbles',
        'field': 'fumbles_rec',
        'yds': 'fumbles_rec_yds',
        'super': [],
        'value': 1,
        'desc': 'Fumble recovery',
    },
    56: {
        'cat': 'fumbles',
        'field': 'fumbles_rec_tds',
        'yds': 'fumbles_rec_yds',
        'super': ['fumbles_rec'],
        'value': 1,
        'desc': 'Fumble recovery touchdown',
    },
    57: {
        'cat': 'fumbles',
        'field': None,
        'yds': '',
        'super': [],
        'value': 0,
        'desc': 'Unknown (redundant with 53? incorrect negative yards?)',
    },
    59: {
        'cat': 'defense',
        'field': 'defense_frec',
        'yds': 'defense_frec_yds',
        'super': [],
        'value': 1,
        'desc': 'Defensive fumble recovery return',
    },
    60: {
        'cat': 'defense',
        'field': 'defense_frec_tds',
        'yds': 'defense_frec_yds',
        'super': ['defense_frec'],
        'value': 1,
        'desc': 'Defensive fumble recovery return touchdown',
    },
    61: {
        'cat': 'lateral',
        'field': 'lateral_fumble_rec',
        'yds': 'lateral_fumble_rec_yds',
        'super': [],
        'value': 1,
        'desc': 'Lateral catch after fumble recovery',
    },
    62: {
        # This is a guess.
        'cat': 'lateral',
        'field': 'lateral_fumble_rec_tds',
        'yds': 'lateral_fumble_rec_yds',
        'super': ['lateral_fumble_rec'],
        'value': 1,
        'desc': 'Lateral catch after fumble recovery for touchdown',
    },
    63: {
        'cat': 'defense',
        'field': 'defense_blk_yds',
        'yds': 'defense_blk_yds',
        'super': [],
        'value': 0,
        'desc': 'FG/Punt block return',
    },
    64: {
        'cat': 'defense',
        'field': 'defense_blk_tds',
        'yds': 'defense_blk_yds',
        'super': [],
        'value': 1,
        'desc': 'FG/Punt block return',
    },
    68: {
        'cat': 'team',
        'field': 'timeout',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Timeout',
    },
    69: {
        'cat': 'kicking',
        'field': 'kicking_fgmissed',
        'yds': 'kicking_fgmissed_yds',
        'super': ['kicking_fga'],
        'value': 1,
        'desc': 'Field goal missed',
    },
    70: {
        'cat': 'kicking',
        'field': 'kicking_fgm',
        'yds': 'kicking_fgm_yds',
        'super': ['kicking_fga'],
        'value': 1,
        'desc': 'Field goal good',
    },
    71: {
        'cat': 'kicking',
        'field': 'kicking_fgb',
        'yds': 'kicking_fgb_yds',
        'super': ['kicking_fga'],
        'value': 1,
        'desc': 'Field goal blocked',
    },
    72: {
        'cat': 'kicking',
        'field': 'kicking_xpmade',
        'yds': '',
        'super': ['kicking_xpa'],
        'value': 1,
        'desc': 'PAT good',
    },
    73: {
        'cat': 'kicking',
        'field': 'kicking_xpmissed',
        'yds': '',
        'super': ['kicking_xpa'],
        'value': 1,
        'desc': 'PAT failed',
    },
    74: {
        'cat': 'kicking',
        'field': 'kicking_xpb',
        'yds': '',
        'super': ['kicking_xpa', 'kicking_xpmissed'],
        'value': 1,
        'desc': 'PAT blocked',
    },
    75: {
        'cat': 'rushing',
        'field': 'rushing_twoptm',
        'yds': '',
        'super': ['rushing_twopta'],
        'value': 1,
        'desc': '2pt conversion successful (rush)',
    },
    76: {
        'cat': 'rushing',
        'field': 'rushing_twoptmissed',
        'yds': '',
        'super': ['rushing_twopta'],
        'value': 1,
        'desc': '2pt conversion failed (rush)',
    },
    77: {
        'cat': 'passing',
        'field': 'passing_twoptm',
        'yds': '',
        'super': ['passing_twopta'],
        'value': 1,
        'desc': '2pt conversion successful (pass)',
    },
    78: {
        'cat': 'passing',
        'field': 'rushing_twoptmissed',
        'yds': '',
        'super': ['rushing_twopta'],
        'value': 1,
        'desc': '2pt conversion failed (pass)',
    },
    79: {
        'cat': 'defense',
        'field': 'defense_tkl',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Tackle',
    },
    80: {
        'cat': 'defense',
        'field': 'defense_tkl_primary',
        'yds': '',
        'super': ['defense_tkl'],
        'value': 1,
        'desc': 'Tackle (primary)',
    },
    82: {
        'cat': 'defense',
        'field': 'defense_ast',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Tackle (assist)',
    },
    83: {
        'cat': 'defense',
        'field': 'defense_sk',
        'yds': 'defense_sk_yds',
        'super': [],
        'value': 1,
        'desc': 'Sack',
    },
    84: {
        'cat': 'defense',
        'field': 'defense_sk_split',
        'yds': 'defense_sk_yds',
        'super': ['defense_sk'],
        'value': 0.5,
        'desc': 'Sack (split)',
    },
    85: {
        'cat': 'defense',
        'field': 'defense_pass_def',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Pass defended',
    },
    86: {
        'cat': 'defense',
        'field': 'defense_puntblk',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Punt blocked',
    },
    87: {
        'cat': 'defense',
        'field': 'defense_xpblk',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'PAT blocked',
    },
    88: {
        'cat': 'defense',
        'field': 'defense_fgblk',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Blocked field goal',
    },
    89: {
        'cat': 'defense',
        'field': 'defense_safe',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Safety',
    },
    91: {
        'cat': 'defense',
        'field': 'defense_ffum',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Forced fumble',
    },
    93: {
        'cat': 'penalty',
        'field': 'penalty',
        'yds': 'penalty_yds',
        'super': [],
        'value': 1,
        'desc': 'Penalty',
    },
    95: {
        'cat': 'team',
        'field': 'rush_loss',
        'yds': 'rush_loss_yds',
        'super': [],
        'value': 1,
        'desc': 'Unknown (rush resulting in loss of yards)',
    },
    102: {
        'cat': 'team',
        'field': 'onside_failed',
        'yds': '',
        'super': ['onside_att'],
        'value': 1,
        'desc': 'Onside kick failed',
    },
    104: {
        'cat': 'receiving',
        'field': 'receiving_twoptm',
        'yds': '',
        'super': ['receiving_twopta'],
        'value': 1,
        'desc': '2pt conversion successful (reception)',
    },
    105: {
        'cat': 'receiving',
        'field': 'receiving_twoptmissed',
        'yds': '',
        'super': ['receiving_twopta'],
        'value': 1,
        'desc': '2pt conversion failed (reception)',
    },
    106: {
        'cat': 'fumbles',
        'field': 'fumbles_lost',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Fumble lost',
    },
    107: {
        'cat': 'kicking',
        'field': 'kicking_onside_rec',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Onside kick recovery',
    },
    110: {
        'cat': 'defense',
        'field': 'defense_qbtkl',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Tackled QB (including sacks)',
    },
    111: {
        'cat': 'passing',
        'field': 'passing_cmp_airyds',
        'yds': 'passing_cmp_airyds',
        'super': [],
        'value': 0,
        'desc': 'Completed yards (in the air)',
    },
    112: {
        'cat': 'passing',
        'field': 'passing_incmp_airyds',
        'yds': 'passing_incmp_airyds',
        'super': [],
        'value': 0,
        'desc': 'Passing yards (in the air; incomplete)',
    },
    113: {
        'cat': 'receiving',
        'field': 'receiving_yac',
        'yds': 'receiving_yac',
        'super': [],
        'value': 0,
        'desc': 'Yards after the catch',
    },
    115: {
        'cat': 'receiving',
        'field': 'receiving_tar',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Target',
    },
    120: {
        'cat': 'defense',
        'field': 'defense_tkl_loss',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'Tackle (for loss of yards)',
    },
    301: {
        'cat': 'team',
        'field': 'xp_aborted',
        'yds': '',
        'super': [],
        'value': 1,
        'desc': 'PAT aborted',
    },
    402: {
        'cat': 'defense',
        'field': 'defense_tkl_loss_yds',
        'yds': 'defense_tkl_loss_yds',
        'super': [],
        'value': 0,
        'desc': 'Tackle yard loss',
    },
}