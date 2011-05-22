# -*- coding: utf-8 -*-
"""
    strings.py
    ~~~~~~~~~~

    Special variables that need i18n love and can't be stored elsewhere.

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""
from flaskext.babel import lazy_gettext as _

SUBJECT_FIELDS = [
    ('11', _('Logic')),
    ('1101', _('Application of logic')),
    ('1102', _('Deductive logic')),
    ('1103', _('General logic')),
    ('1104', _('Inductive logic')),
    ('1105', _('Methodology')),
    ('1199', _('Other specialities relating to logic')),

    ('12', _('Mathematics')),
    ('1201', _('Algebra')),
    ('1202', _('Analysis and functional analysis')),
    ('1203', _('Computer Sciences')),
    ('1204', _('Geometry')),
    ('1205', _('Number Theory')),
    ('1206', _('Numerical analysis')),
    ('1207', _('Operations research')),
    ('1208', _('Probability')),
    ('1209', _('Statistics')),
    ('1210', _('Topology')),
    ('1299', _('Other mathematical specialities')),

    ('22', _('Physics')),
    ('2201', _('Acoustics')),
    ('2202', _('Electro-magnetism')),
    ('2203', _('Electronics')),
    ('2204', _('Fluids (physics of)')),
    ('2205', _('Mechanics')),
    ('2206', _('Molecular physics')),
    ('2207', _('Nuclear physics')),
    ('2208', _('Nucleonics')),
    ('2209', _('Optics')),
    ('2210', _('Physical chemistry')),
    ('2211', _('Solid state physics')),
    ('2212', _('Theoretical physics')),
    ('2213', _('Thermodynamics')),
    ('2214', _('Units and constants')),
    ('2290', _('High energy physics')),
    ('2299', _('Other physical specialities')),

    ('23', _('Chemistry')),
    ('2301', _('Analytical chemistry')),
    ('2302', _('Biochemistry')),
    ('2303', _('Inorganic chemistry')),
    ('2304', _('Macromolecular chemistry')),
    ('2305', _('Nuclear chemistry')),
    ('2306', _('Organic chemistry')),
    ('2307', _('Physical chemistry')),
    ('2399', _('Other chemical specialities')),

    ('24', _('Life sciences')),
    ('2401', _('Animal Biology (Zoology)')),
    ('2402', _('Anthropology (physical)')),
    ('2403', _('Biochemistry')),
    ('2404', _('Biomathematics')),
    ('2405', _('Biometrics')),
    ('2406', _('Biophysics')),
    ('2407', _('Cell biology')),
    ('2408', _('Ethology')),
    ('2409', _('Genetics')),
    ('2410', _('Human biology')),
    ('2411', _('Human physiology')),
    ('2412', _('Immunology')),
    ('2413', _('Insect biology')),
    ('2414', _('Microbiology')),
    ('2415', _('Molecular biology')),
    ('2416', _('Palaeontology')),
    ('2417', _('Plant Biology (Botany)')),
    ('2418', _('Radiobiology')),
    ('2419', _('Symbiosis')),
    ('2420', _('Virology')),
    ('2490', _('Neurosciences')),
    ('2499', _('Other biological specialities')),

    ('25', _('Earth and Space Sciences')),
    ('2501', _('Atmospheric sciences')),
    ('2502', _('Climatology')),
    ('2503', _('Geochemistry')),
    ('2504', _('Geodesy')),
    ('2505', _('Geography')),
    ('2506', _('Geology')),
    ('2507', _('Geophysics')),
    ('2508', _('Hydrology')),
    ('2509', _('Meteorology')),
    ('2510', _('Oceanography')),
    ('2511', _('Soil Science')),
    ('2512', _('Space Sciences')),
    ('2599', _('Other Earch, Space or Environmental specialities')),

    ('32', _('Medical Sciences')),
    ('3201', _('Clinical sciences')),
    ('3202', _('Epidemiology')),
    ('3203', _('Forensic medicine')),
    ('3204', _('Occupational medicine')),
    ('3205', _('Internal medicine')),
    ('3206', _('Nutritional sciences')),
    ('3207', _('Pathology')),
    ('3208', _('Pharmacodynamics')),
    ('3209', _('Pharmacology')),
    ('3210', _('Preventive medicine')),
    ('3211', _('Psychiatry')),
    ('3212', _('Public health')),
    ('3213', _('Surgery')),
    ('3214', _('Toxicology')),
    ('3299', _('Other medical specialities')),

    ('33', _('Technological Sciences')),
    ('3301', _('Aeronautical technology and engineering')),
    ('3302', _('Biochemical technology')),
    ('3303', _('Chemical technology and engineering')),
    ('3304', _('Computer technology')),
    ('3305', _('Construction technology')),
    ('3306', _('Electrical technology and engineering')),
    ('3307', _('Electronic technology')),
    ('3308', _('Environmental technology and engineering')),
    ('3309', _('Food technology')),
    ('3310', _('Industrial technology')),
    ('3311', _('Instrumentation technology')),
    ('3312', _('Materials technology')),
    ('3313', _('Mechanical engineering and technology')),
    ('3314', _('Medical technology')),
    ('3315', _('Metallurgical technology')),
    ('3316', _('Metal products technology')),
    ('3317', _('Motor vehicle technology')),
    ('3318', _('Mining technology')),
    ('3319', _('Naval techonology')),
    ('3320', _('Nuclear technology')),
    ('3321', _('Petroleum and coal technology')),
    ('3322', _('Power technology')),
    ('3323', _('Railway technology')),
    ('3324', _('Space technology')),
    ('3325', _('Telecommunications technology')),
    ('3326', _('Textile technology')),
    ('3327', _('Transportation systems technology')),
    ('3328', _('Unit operations technology')),
    ('3329', _('Urban planning')),
    ('3399', _('Other technological specialities')),

    ('51', _('Anthropology')),
    ('5101', _('Cultural anthropology')),
    ('5102', _('Ethnography and Ethnology')),
    ('5103', _('Social anthropology')),
    ('5199', _('Other anthropological specialities')),

    ('53', _('Economic Sciences')),
    ('5301', _('Domestic fiscal policy and public finance')),
    ('5302', _('Econometrics')),
    ('5303', _('Economic accounting')),
    ('5304', _('Economic activity')),
    ('5305', _('Economic systems')),
    ('5306', _('Economics of technological change')),
    ('5307', _('Economic theory')),
    ('5308', _('General economics')),
    ('5309', _('Industrial organization and public policy')),
    ('5310', _('International economics')),
    ('5311', _('Organization and management of enterprises')),
    ('5312', _('Sectorial economics')),
    ('5399', _('Other economics specialities')),

    ('56', _('Juridical Sciences & Law')),
    ('5601', _('Canon law')),
    ('5602', _('General theory and methods')),
    ('5603', _('International law')),
    ('5604', _('Legal organization')),
    ('5605', _('National law and legislation')),
    ('5699', _('Other juridical specialities')),

    ('57', _('Linguistics')),
    ('5701', _('Applied linguistics')),
    ('5702', _('Diachronic linguistics')),
    ('5703', _('Linguistic geography')),
    ('5704', _('Linguistic theory')),
    ('5705', _('Synchronic linguistics')),
    ('5799', _('Other linguistic specialities')),

    ('58', _('Pedagogy')),
    ('5801', _('Educational theory and methods')),
    ('5802', _('Organization and planning of education')),
    ('5803', _('Teacher training and employment')),
    ('5899', _('Other pedagogical specialities')),

    ('61', _('Psychology')),
    ('6101', _('Abnormal psychology')),
    ('6102', _('Adolescent and child psychology')),
    ('6103', _('Counselling and guidance')),
    ('6104', _('Educational psichology')),
    ('6105', _('Evaluation and measurement in psychology')),
    ('6106', _('Experimental psychology')),
    ('6107', _('General psychology')),
    ('6108', _('Geriatric psychology')),
    ('6109', _('Occupational and personnel psychology')),
    ('6110', _('Parapsychology')),
    ('6111', _('Personality')),
    ('6112', _('Psychological study of social issues')),
    ('6113', _('Psychopharmacology')),
    ('6114', _('Social psychology')),
    ('6199', _('Other psychological specialities')),

    ('71', _('Ethics')),
    ('7101', _('Classical ethics')),
    ('7102', _('Ethics of individuals')),
    ('7103', _('Group ethics')),
    ('7104', _('Prospective ethics')),
    ('7199', _('Other specialities relating to ethics')),

    ('72', _('Philosophy')),
    ('7201', _('Philosophy of knowledge')),
    ('7202', _('Philosophical anthropology')),
    ('7203', _('General philosophy')),
    ('7204', _('Philosophical systems')),
    ('7205', _('Philosophy of science')),
    ('7206', _('Philosophy of nature')),
    ('7207', _('Social philosophy')),
    ('7208', _('Philosophical doctrines')),
    ('7299', _('Other philosophical specialities')),
    ('72', _('Philosophy')),
]

NORMATIVE_AUTHORIZATIONS = [
    ('standardizedTerm', _('Standard')),
    ('preferredTerm', _('Preferred')),
    ('admittedTerm', _('Admitted')),
    ('deprecatedTerm', _('Deprecated')),
    ('supersededTerm', _('Superseded')),
    ('legalTerm', _('Legal')),
    ('regulatedTerm', _('Regulated')),
    ('encodedTerm', _('Encoded')),
    ('usedTerm', _('Used'))
]

TERM_TYPES = [
    ('abbreviation', _('Abbreviation')),
    ('acronym', _('Acronym')),
    ('clippedTerm', _('Clipped term')),
    ('commonName', _('Common name')),
    ('entryTerm', _('Entry term')),
    ('equation', _('Equation')),
    ('formula', _('Formula')),
    ('fullForm', _('Full form')),
    ('initialism', _('Initialism')),
    ('internationalism', _('Internationalism')),
    ('internationalScientificTerm', _('International scientific term')),
    ('logicalExpression', _('Logical expression')),
    ('partNumber', _('Part number')),
    ('phraseologicalUnit', _('Phraseological unit')),
    ('transcribedForm', _('Transcribed form')),
    ('transliteratedForm', _('Transliterated form')),
    ('shortForm', _('Short form')),
    ('shortcut', _('Shortcut')),
    ('sku', _('SKU (Stock Keeping Unit)')),
    ('standardText', _('Standard text')),
    ('string', _('String')),
    ('symbol', _('Symbol')),
    ('synonym', _('Synonym')),
    ('synonymousPhrase', _('Synonymous phrase')),
    ('variant', _('Variant')),
    ('other', _('Other')),
]

PART_OF_SPEECH = [
    ('noun', _('Noun')),
    ('verb', _('Verb')),
    ('adjective', _('Adjective')),
    ('adverb', _('Adverb')),
    ('properNoun', _('Proper noun')),
    ('other', _('Other')),
]

PRODUCT_SUBSET = [
    ('0', _('Notes')),
    ('1', _('End of degree projects')),
    ('2', _('Research projects')),
    ('3', _('Theses')),
]

WORKING_STATUS = [
    ('importedElement', _('Imported')),
    ('starterElement', _('Starter')),
    ('workingElement', _('Working')),
    ('consolidatedElement', _('Consolidated')),
    ('archiveElement', _('Archived')),
]

ADMINISTRATIVE_STATUS = [
    ('preferredTerm-admn-sts', _('Preferred')),
    ('admittedTerm-admn-sts', _('Admitted')),
    ('deprecatedTerm-admn-sts', _('Deprecated')),
    ('supersededTerm-admn-sts', _('Superseded')),
]
