# prerequisites.py

import pandas as pd

def apply_prerequisites(res: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply prerequisite rules to produce 0/1 flags per subject in df.
    Expects:
      - res: rows per student with columns like StuID, Y, CG, and subject-specific fields
      - df:  rows per student with a column 'Student ID' matching res['StuID']
    Returns:
      - df with new subject flag columns (int 0/1)
    """

    # -----------------
    # Helper utilities
    # -----------------
    def sget(col, default=False):
        """Safe column getter aligned to res.index."""
        if col in res:
            return res[col]
        # if default is a scalar or list-like of acceptable grades
        return pd.Series(default, index=res.index)

    def set_flag(mask, colname):
        """Set flag on df for students satisfying mask."""
        valid_students = res.loc[mask, 'StuID'].unique()
        df[colname] = df['Student ID'].isin(valid_students).astype(int)

    # -------------
    # Base masks
    # -------------
    new5  = res['CG'].isin(['N5'])
    new4  = res['CG'].isin(['N4', 'N5'])
    new3  = res['CG'].isin(['N3', 'N4', 'N5'])
    new   = res['CG'].isin(['N2', 'N3', 'N4', 'N5'])
    cgtop3 = res['CG'].isin(['B+', 'A', 'A+'])
    cgtop4 = res['CG'].isin(['B', 'B+', 'A', 'A+'])

    y6  = res['Y'] == 6
    y7  = res['Y'] == 7
    y8  = res['Y'] == 8
    y9  = res['Y'] == 9
    y10 = res['Y'] == 10
    y11 = res['Y'] == 11
    y12 = res['Y'] == 12

    early_VCE      = (y9) & ((res['CG'].isin(['D+', 'C', 'C+', 'B', 'B+', 'A', 'A+'])) | new3)
    early_VCE_mid  = (y9) & ((res['CG'].isin(['B', 'B+', 'A', 'A+'])) | new5)
    early_VCE_high = (y9) & ((res['CG'].isin(['A', 'A+'])) | new5)

    art_high = (y9) & cgtop3 & (
        sget('ARDE').isin(['A', 'A+']) | sget('DRPA').isin(['A', 'A+']) |
        sget('GRDE').isin(['A', 'A+']) | sget('PHO').isin(['A', 'A+']) |
        sget('SCME').isin(['A', 'A+']) | sget('SCPR').isin(['A', 'A+'])
    )
    hum_high = (y9) & cgtop3 & (
        sget('HIS1').isin(['A', 'A+']) | sget('RV3').isin(['A', 'A+']) |
        sget('GEO1').isin(['A', 'A+']) | sget('EB').isin(['A', 'A+'])
    )
    mat_high = (y9) & cgtop3 & (sget('AMAT1').isin(['A+']) | new5)
    sci_high = (y9) & cgtop3 & (sget('RSC1').isin(['A', 'A+']) | new5)

    pe_high = (y9) & cgtop3 & (
        sget('HPE3').isin(['A', 'A+']) |
        sget('DE').isin(['A', 'A+'])   |
        sget('RFIT').isin(['A', 'A+'])
    )

    mat_high10 = (y10) & (
        (sget('IMAT2').isin(['A', 'A+']) & (sget('IMAT3') == 'S2')) |
        sget('AMAT2').isin(['B+', 'A', 'A+'])
    )
    mat_mid10 = (y10) & (
        (sget('IMAT2').isin(['B+', 'A', 'A+']) & (sget('IMAT3') == 'S2')) |
        sget('AMAT2').isin(['B', 'B+', 'A', 'A+'])
    )
    sci_mid10 = (y10) & (sget('SCI4').isin(['B', 'B+', 'A', 'A+']) | sget('RSC1').isin(['B', 'B+', 'A', 'A+']))
    sci_minmid10 = (y10) & (sget('SCI4').isin(['C+', 'B', 'B+', 'A', 'A+']) | sget('RSC1').isin(['C+', 'B', 'B+', 'A', 'A+']))
    sci_min10 = (y10) & (sget('SCI4').isin(['C', 'C+', 'B', 'B+', 'A', 'A+']) | sget('RSC1').isin(['C', 'C+', 'B', 'B+', 'A', 'A+']))

    # ##############
    # ### Year 7 ###
    # ##############
    for subj in [
        'Design and Technologies', 'Digital Technologies', 'Drama 1', 'English 1',
        'Health and Physical Education 1', 'Humanities 1', 'Mathematics 1',
        'Music 1', 'Religion and Values 1', 'Science 1', 'Visual Arts 1'
    ]:
        set_flag(y6, subj)

    set_flag(y6 & (sget('ARA').isin(['C5','C4','C3','C2','C1','B2','B1','A']) | new), 'Arabic 1')
    set_flag((y6 | y7 | y8) & new, 'Turkish 1')
    set_flag((y6 & (sget('TUR') != '')) | (y7 & (sget('TUR1') != '')) | (y6 & sget('BTUR').isin(['A','B1','B2'])), 'Turkish 2')
    set_flag(y6 & (sget('ATUR') != ''), 'Turkish 5')

    # ##############
    # ### Year 8 ###
    # ##############
    for subj in [
        'Drama 2', 'English 2', 'Food Technology', 'Health and Physical Education 2',
        'Humanities 2', 'Mathematics 2', 'Media', 'Music 2', 'Programming',
        'Religion and Values 2', 'Robotics 1', 'Science 2', 'Textiles', 'Visual Arts 2'
    ]:
        set_flag(y7, subj)

    set_flag((sget('ARA1') != '') | (y7 & new), 'Arabic 2')
    set_flag((sget('TUR2') != '') & (y7 | y8), 'Turkish 3')
    set_flag((sget('TUR5') != '') & y7, 'Turkish 6')

    # ##############
    # ### Year 9 ###
    # ##############
    for subj in [
        'English 3', 'Health and Physical Education 3', 'History 1',
        'Intermediate Mathematics 1', 'Religion and Values 3', 'Science 3'
    ]:
        set_flag(y8, subj)

    set_flag(y8 & ((sget('MAT2').isin(['A','A+'])) | new5), 'Advanced Mathematics 1')
    set_flag((sget('ARA2') != '') | (y8 & new), 'Arabic 3')
    set_flag((sget('ARDE') == '') & (y8 | y9), 'Architecture and Design')
    set_flag((y8 | y9), 'Behavioural Science')  # placeholder for 2027 condition with BSC
    set_flag((sget('CC') == '') & (y8 | y9), 'Civics and Citizenship')
    set_flag(y8 | y9, 'Debating and Public Speaking')
    set_flag(y8 | y9, 'Drama 3')
    set_flag((sget('DRPA') == '') & (y8 | y9), 'Drawing and Painting')
    set_flag(y8 | y9, 'Duke of Edinburgh')
    set_flag((sget('EB') == '') & (y8 | y9), 'Economics and Business')
    set_flag((sget('FATT') == '') & (y8 | y9), 'Fashion and Textile Trends')
    set_flag((sget('FI') == '') & (y8 | y9), 'Food and the Food Industry')
    set_flag((sget('GEO1') == '') & (y8 | y9), 'Geography 1')
    set_flag((sget('GRDE') == '') & (y8 | y9), 'Graphic Design')
    set_flag((sget('INN') == '') & (y8 | y9), 'Innovation')
    set_flag((y8 | y9), 'Introduction to Artificial Intelligence')  # placeholder for 2027 IAI gating
    set_flag(y8 | y9, 'Music 3')
    set_flag((sget('PHO') == '') & (y8 | y9), 'Photography')
    set_flag((sget('RFIT') == '') & (y8 | y9) & (sget('HPE2').isin(['C','C+','B','B+','A','A+']) | sget('HPE3').isin(['C','C+','B','B+','A','A+']) | new5), 'Recreational Fitness')
    set_flag((sget('RMAT') == '') & (y8 | y9), 'Recreational Mathematics')

    set_flag((y8 & (sget('SCI2').isin(['B+','A','A+']) | new4)) | (y9 & (sget('SCI3').isin(['C+','B','B+','A','A+']) | new4)), 'Research Science 1')
    set_flag((y8 & (sget('SCI2').isin(['B+','A','A+']) | new4)), 'Research Science 2')

    set_flag((sget('ROB2') == '') & (y8 | y9), 'Robotics 2')
    set_flag((sget('SCME') == '') & (y8 | y9), 'Screen and Media')
    set_flag((sget('SCPR') == '') & (y8 | y9), 'Sculpture and Printmaking')

    if 'SVF' in res:
        set_flag((sget('SVF') == '') & (y8 | y9), 'Social Values in Film')
    else:
        df['Social Values in Film'] = 0

    set_flag((y8 | y9), 'Stagecraft and Production')   # placeholder for 2027 STPRO gating
    set_flag((y8 | y9), 'Technology Start-Ups')       # placeholder for 2027 TECS gating
    set_flag((sget('TUR6') != '') & y8, 'Turkish 7')
    set_flag((sget('VS') == '') & (y8 | y9), 'Volunteering Skills')
    set_flag((sget('WDCS') == '') & (y8 | y9), 'Web Design and Cyber Security')

    # ###############
    # ### Year 10 ###
    # ###############
    for subj in [
        'Certificate II in Workplace Skills', 'English 4', 'Health and Physical Education 4',
        'History 2', 'Intermediate Mathematics 2', 'Intermediate Mathematics 3',
        'Religion Studies', 'Science 4'
    ]:
        set_flag(y9, subj)

    set_flag(y9 & (((sget('ENG3').isin(['B','B+','A','A+'])) & cgtop4) | new4), 'Advanced English')
    set_flag(y9 & (sget('AMAT1').isin(['C','C+','B','B+','A','A+']) | sget('IMAT1').isin(['A','A+']) | new5), 'Advanced Mathematics 2')
    set_flag(y9 & (sget('AMAT1').isin(['C','C+','B','B+','A','A+']) | sget('IMAT1').isin(['A','A+']) | new5), 'Extended Mathematics')

    # ###############
    # ### Unit 1-2 ###
    # ###############
    for subj in [
        'Drama U12', 'English Language U12', 'English U12', 'General Mathematics U12',
        'Literature U12', 'VCE VET Business U12', 'VCE VET Sport and Recreation U12'
    ]:
        set_flag(y10, subj)

    set_flag(y10 | early_VCE_high | art_high, 'Art Creative Practice U12')
    set_flag(y10 | early_VCE_high | art_high, 'Theatre Studies U12')
    set_flag(y10 | early_VCE_high | art_high, 'Visual Communication Design U12')

    set_flag(y10 | early_VCE_high | hum_high, 'Economics U12')
    set_flag(y10 | early_VCE_high | hum_high, 'History U12')
    set_flag(y10 | early_VCE_high | hum_high, 'Legal Studies U12')
    set_flag(y10 | early_VCE_high | hum_high, 'Texts and Traditions U12')
    set_flag(y10 | early_VCE_high | hum_high, 'Politics U12')
    set_flag(y10 | early_VCE_high | hum_high, 'Sociology U12')

    set_flag((y10 & (sci_mid10 | new4)) | (early_VCE_high & sci_high) | (new5 & (y9 | y10)), 'Chemistry U12')
    set_flag((y10 & (sci_minmid10 | new4)) | (early_VCE_high & sci_high) | (new5 & (y9 | y10)), 'Physics U12')

    set_flag((sget('ACOMU12') == '') & (y10 | early_VCE), 'Applied Computing U12')

    set_flag((y9 & cgtop4 & (sget('SCI3').isin(['B+','A','A+']) | (sget('RSC1') != ''))) | (y9 & new4) | (y10 & new4) | (y10 & sci_min10 & (sget('BIOU12') == '')), 'Biology U12')

    set_flag((sget('BMU12') == '') & (y10 | early_VCE), 'Business Management U12')
    set_flag((sget('HHDU12') == '') & (y10 | early_VCE), 'Health and Human Development U12')

    set_flag((y10 & (mat_mid10 | new4)) | (early_VCE_high & mat_high) | (new5 & (y9 | y10)), 'Mathematical Methods U12')

    set_flag(y10 | early_VCE_high | pe_high, 'Outdoor and Environmental Studies U12')
    set_flag(y10 | early_VCE_high | pe_high, 'Physical Education U12')

    set_flag(y10 | early_VCE_mid, 'Product Design and Technologies U12')

    set_flag((y9 & cgtop4 & (sget('SCI3').isin(['B','B+','A','A+']) | (sget('RSC1') != ''))) | (y9 & new4) | (y10 & new4) | (y10 & sci_min10 & (sget('PSYU12') == '')), 'Psychology U12')

    set_flag((y10 & (mat_high10 | new4)) | (new5 & y10), 'Specialist Mathematics U12')
    set_flag((y9 | y10) & (sget('TUR7') != ''), 'Turkish U12')

    # ###############
    # ### Unit 3-4 ###
    # ###############
    # Accounting U34 intentionally commented out in provided rules

    set_flag((sget('ACPU12') != ''), 'Art Creative Practice U34')
    set_flag((sget('BIOU12') != ''), 'Biology U34')
    set_flag((sget('BMU12') != ''), 'Business Management U34')
    set_flag((sget('CHEU12') != ''), 'Chemistry U34')

    set_flag((sget('ACOMU12') != ''), 'Data Analytics U34')
    set_flag((sget('ACOMU12') != ''), 'Software Development U34')

    set_flag((sget('DRAU12') != ''), 'Drama U34')
    set_flag((sget('ECOU12') != ''), 'Economics U34')

    # Any U12 English qualifies for U34 English streams
    cols = ['ENGU12', 'ELANU12', 'LITU12']
    mask_any_u12_english = pd.Series(False, index=res.index)
    for col in cols:
        if col in res:
            mask_any_u12_english |= (res[col] != '')
    set_flag(mask_any_u12_english, 'English U34')
    set_flag(mask_any_u12_english, 'English Language U34')
    set_flag(mask_any_u12_english, 'Literature U34')

    set_flag((sget('GMATU12') != '') | (sget('MATMU12') != '') | mat_high10 | (y10 & new4), 'General Mathematics U34')
    set_flag((sget('HHDU12') != ''), 'Health and Human Development U34')
    set_flag((sget('HISU12') != ''), 'History U34')
    set_flag((sget('LEGU12') != ''), 'Legal Studies U34')
    set_flag((sget('MATMU12') != ''), 'Mathematical Methods U34')
    set_flag((sget('PEU12') != ''), 'Physical Education U34')
    set_flag((sget('PHYU12') != ''), 'Physics U34')
    set_flag((sget('PSYU12') != ''), 'Psychology U34')
    set_flag((sget('SMATU12') != '') | (y11 & sget('MATMU12').isin(['B+','A','A+'])) | (y11 & new5), 'Specialist Mathematics U34')
    set_flag((sget('TURU12') != ''), 'Turkish U34')
    set_flag((sget('VBUSU12') != ''), 'VCE VET Business U34')
    set_flag((sget('VSRU12') != ''), 'VCE VET Sport and Recreation U34')
    set_flag((sget('VCDU12') != ''), 'Visual Communication Design U34')

    return df

