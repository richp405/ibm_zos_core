# -*- coding: utf-8 -*-


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION=r"""
module: zos_mvs_raw 
author:
    - Xiao Yuan Ma bjmaxy@cn.ibm.com"
short_description: Run a z/OS program  
version_added: "2.9"
options:
    program_name: 
        description: The name of the z/OS program that will be run
        required: true
        type: str
        samples: IDCAMS, IEFBR14, IEBGENER, etc.
    parms: 
        description:
            - The program arguments, e.g. -a='MARGINS(1,72)'. 
        required: false
        type: str
    auth:
        description: 
            - Instruct whether this program should run authorized or not. 
            - If set to true, the program will be run as APF authorized, otherwise the program runs as unauthorized.
        required: false
        type: bool
        default: false
    dds:
        description:
            - Specify the input data source.
            - Here we support 5 kinds of source: 
                - dd_dataset for dataset files, 
                - dd_uss for uss files, 
                - dd_input for the direct input content, like stdin, 
                - dd_sysout for the output, like stdout, 
                - dd_dummy for no content input. 
            - In dds, it support combination of all/any of these kinds of the data input source.  
        required: false
        type: list
        elements: dict
        contains:
            dd_dataset:
                description:
                    - Specify the dataset input information.
                    - User can use existing dataset or create new dataset. 
                required: false
                type: dict
                suboptions:                 
                    dd_name:
                        description: The dd name.
                        required: true
                        type: str
                    data_set_name:
                        description: The dataset name.
                        type: str
                        required: false
                    data_set_type:
                        description: The dataset type.
                        type: str
                        choice:
                            - library
                            - library_1
                            - library_2
                            - hfs
                            - pds
                            - pipe
                            - extreq
                            - extpref
                            - large
                            - basic
                    disposition:
                        description: 
                            - Disposition indicts the status of a data set .
                        type: str
                        default: shr
                        required: false
                        choice:
                            - new
                            - shr
                            - mod
                            - old
                    disposition_normal:
                        description:
                            - This tell the system what to do with the data set after normal termination of the program.
                        type: str
                        required: false
                        choice:
                            - del
                            - keep
                            - catlog 
                            - uncatalog
                    disposition_abnormal:
                        description:
                            - This tell the system what to do with the data set after abnormal termination of the 
                              program.
                        type: str
                        required: false
                        choice:
                            - del
                            - keep
                            - catlog 
                            - uncatalog
                    space_type:
                        description:
                            - The space type for a new requested data set.
                        type: str
                        required: false
                        choice:
                            - trk
                            - cyl
                            - blklgth
                            - reclgth
                    space_primary:
                        description: 
                            - The first allocated space size of a new dataset.
                            - The space unit is using the one space_type specified. 
                        type: int
                    space_secondary:
                        description:
                            - If the primary dataset is not enough, it can obtain additional space.
                            - The space unit is using the one space_type specified. 
                        type: int           
                    volume:
                        description:
                            - Identify the volume or volumes on which a data set resides or will reside.
                        type: list [str]
                        required: false
                    sms_management_class:
                        description:  
                            - Specify a management class for a new SMS-managed data set 
                            - It is ignored if you specify it for an existing data set.
                            - All values must be between 1-8 alpha-numeric chars
                        type: str
                    sms_storage_class:
                        description:
                            - Specify a storage class for a new SMS-managed data set.
                            - It is ignored if you specify it for an existing data set.
                            - All values must be between 1-8 alpha-numeric chars
                        type: str
                    sms_data_class:
                        description:
                            - Specify a data class for a new data set.
                            - It is ignored if you specify it for an existing data set. 
                            - All values must be between 1-8 alpha-numeric chars
                        type: str
                    block_size:
                        description:  
                            - specify the maximum length of a block.
                            - size in bytes, K, M, G
                        type: str
                        sample: 23472, 204K
                    data_set_key_label:
                        description: 
                            - Use this label option to specify for a tape or direct access data set:
                                1. The type and contents of the label or labels for the data set.
                                2. If a password is required to access the data set. 
                                3. If the system is to open the data set only for input or output. 
                                4. The expiration date or retention period for the data set. 
                        type: str
                    encryption_key_1:
                        description:
                             - Specify the encryption related setting.  
                        type:dict 
                        contains:
                            label:
                                description: 
                                    - Use it to specify the label for the key encrypting key used by the Encryption Key 
                                      Manager.
                                    - Key label must have a private key associated with it.
                                    - up to 64 characters
                                type: str
                            encoding:
                                type: str  
                                choice: 
                                    - L , for label encoding
                                    - H , for hash encoding
                    encryption_key_2:
                        description:  
                            - Specify the encryption related setting.    
                        type:dict 
                        contains:
                            label:
                                description: 
                                    - Use it to specify the label for the key encrypting key used by the Encryption Key 
                                      Manager.
                                    - Key label must have a private key associated with it.
                                    - up to 64 characters
                                type: str
                            encoding:
                                type: str  
                                choice: 
                                    - L , for label encoding
                                    - H , for hash  encoding
                    key_length:
                        description:
                            - Specify the length of the keys used in a new data set.
                            - Or with SMS, override the key length defined in the data class of the data set.
                        type: int (0 -255 non-vsam ), (1-255 vsam)
                    record_length:
                        description:
                            - The logical record length. (e.g C(80))
                            - For variable data sets, the length must include the 4-byte prefix area.
                            - Defaults vary depending on format. If FB/FBA 80, if VB/VBA 137, if U 0
                        type: int    (1-32760 for non-vsam,  1-32761 for vsam) 
                        required: false
                    record_format:
                        description:
                            - Specify the format and characteristics of the records in a new data set.
                            - Choices are case-insensitive.
                        required: false
                        type: str
                        choice:
                            - U
                            - UT
                            - V
                            - VB
                            - VS
                            - VT
                            - VBS
                            - VBT
                            - VBST
                            - F
                            - FB
                            - FT
                            - FBT
                            - D
                            - DB
                            - DS
                            - DBS
                        default: FB(fixed block)
                    return_content:
                        description: 
                        required: false
                        type: str
                        choice:     
                            - none
                            - text    
                            - base64
                        default: none
            dd_sysout:
                description:
                    - Write the output to stdout.
                required: false
                type: dict
                suboptions:  
                    dd_name:
                        description: The dd name. 
                        required: true
                        type: str
            	    return_content:
            	        description:
            	            - Specify whether return the dd_dataset content.
            	            - None means do not return content.
            	            - Text means return value in ASCII, converted from ebcdic. 
            	            - base64 means in binary mode.
            	        required: false
                        type: str
                        choice:    
                            - none
                            - text   
                            - base64 
                    sysout_class: 
                        description: The sysout class. 
                        type: str
                        sample: *, A
            dd_uss:
                description:
                required: false
                type: dict
                suboptions:  
                    dd_name:
                        description: The dd name. 
                        required: true
                        type: str
                    path:
                        description:
                        type: str
                    path_disposition_normal:
                        choice:
                            - keep
                            - delete
                    path_disposition_abnormal
                        choice:
                            - keep
                            - delete
                    path_mode:
                        description: Note to dev, we will leave these posix terms ie SISGID 
                                 Can be any of these, we need to document this:
                                 SIRUSR,SIWUSR,SIXUSR,SIRWXU,SIRGRP,SIWGRP,SIXGRP,SIRWXG,SIROTH,SIWOTH,SIXOTH,SIRWXO,SISUID,SISGID
                        type:list 
                    path_access_group:
                        description: choose one and then set path_status_group.
                        choice:
                            read_only
                            write_only
                            read_write
                    path_status_group:
                        description: You can choose up to 6 of these options (OAPPEND,OCREAT,OEXCL,ONOCTTY,ONONBLOCK,OSYNC,OTRUNC)
                                 //todo: rename the OAPPEND ...OTRUNC to description options
                        type: list [str]
                    file_data:
                        choice:
                            - binary
                            - text 
                            - record
                    return_content:
                        description:
            	            - Specify whether return the dd_dataset content.
            	            - None means do not return content.
            	            - Text means return value in ASCII, converted from ebcdic. 
            	            - base64 means in binary mode. 
                        required: false
                        type: str
                        choice: 
                            - none
                            - text   
                            - base64
                        default: none
            dd_input:
                description:
                    - User can specify the input content directly, like stdin.
                required: false
                type: dict
                suboptions:
                    dd_name:
                        description: The dd name. 
                        required: true
                        type: str
                    dd_content: 
                        description:
                            - Input the content, it supports single or multiple lines input. 
                        required: false
                        type: raw
                        elements: str
                            - LINE 1
                            - LINE 2
                            - LINE 3
                    return_content:
                        description:
            	            - Specify whether return the dd_dataset content.
            	            - None means do not return content.
            	            - Text means return value in ASCII, converted from ebcdic. 
            	            - base64 means in binary mode.
                        required: false
                        type: str
                        choice:      
                            - none
                            - text 
                            - base64
                        default: none
            dd_dummy:
                description:
                     - It supports no content input.  
                required: false
                type: dict
                suboptions: 
                    dd_name:
                        description: The dd name. 
                        required: true
                        type: str 
"""

RETURN = """
ret_code: 
    description: The return code. 
    returned : always
    type: dict
    contains:
        msg:
            description: Holds the return code 
            type: str
        msg_code: 
            description: Holds the return code string 
            type: str
        msg_txt: 
            description: Holds additional information related to the program that may be useful to the user.
            type: str
        code: 
            description: return code converted to integer value (when possible)
            type: int 
    sample: Value 0 indicates success, non-zero indicates failure.
       - code: 0
       - msg: "0"
       - msg_code: "0"
       - msg_txt: "THE z/OS PROGRAM EXECUTION SUCCEED." 
ddnames:
    description: All the related dds with the program. 
    returned: always
    type: list<dict> 
    contains:
        ddname:
          description: data definition name
          type: str
        dataset:
          description: the dataset name  
          type: str
        content:
          description: ddname content
          type: list[str] 
        record_count:
          description: the lines of the content 
          type: int
        byte_count:
          description: bytes count
          type: int
    samples:         
        - ddname: "SYSIN", "SYSPRINT",etc.
        - dataset: "TEST.TESTER.DATA", "stdout", "dummy", etc
        - content: " "
        - record_count: 4
        - byte_count:  415
changed: 
    description: Indicates if any changes were made during module operation.
    type: bool
"""

EXAMPLES = r"""
- name: Run IEFBR14 program. This is a simple program, no output.  
    zos_mvs_raw:
        program_name: IEFBR14

- name: run IDCAMS program to list the catagory of dataset 'TESTER.DATASET'  
    zos_mvs_raw:
        program_name: IDCAMS
        parms:
        auth: true
        dds:
          - dd_input:
              - dd_name: sysin
              - dd_content: LISTCAT ENT('TESTER.DATASET')
              - return_content: text
          - dd_dataset:
              - dd_name: sysprint
              - data_set_name: TESTER.MVSUTIL.PYTHON.OUT
              - disposition: old
              - disposition_normal: keep
              - disposition_abnormal: keep
              - return_content: text

  - name: TSO isrsupc program, multiple lines sysin inputs
    zos_mvs_raw:
      program_name: isrsupc
      parms: DELTAL,SRCHCMP,ANYC
      dds:
        - dd_dataset:
            - dd_name: newdd
            - data_set_name: BJMAXY.IMSTESTL.IMS1.TEST05:BJMAXY.IMSTESTL.IMS1.TEST06
            - disposition: old
            - disposition_normal: keep
            - disposition_abnormal: keep
            - return_content: text
        - dd_input:
            - dd_name: sysin
            - dd_content:
              - "  CMPCOLM 7:71"
              - "  DPLINE  '*',7"
              - "  SRCHFOR 'NEEDLE',W,10:20"
            - return_content: text
        - dd_dataset:
            - dd_name: olddd
            - data_set_name: BJMAXY.IMSTESTL.IMS1.TEST07
            - disposition: old
            - disposition_normal: keep
            - disposition_abnormal: keep
            - return_content: text
        - dd_sysout:
            - dd_name: outdd
            - sysout_class: A
            - return_content: text
              
  - name: TSO iebgener program,This program copy the content from sysut1 to sysut2.
    zos_mvs_raw:
      program_name: iebgener
      dds:
        - dd_dummy:
            - dd_name: sysin
        - dd_dataset:
            - dd_name: sysut1
            - data_set_name: BJMAXY.MVSUTIL.PYTHON.MVSCMD.A
        - dd_dataset:
            - dd_name: sysut2
            - data_set_name: BJMAXY.MVSUTIL.PYTHON.MVSCMD.B
        - dd_sysout:
            - dd_name: sysprint
            - sysout_class: A
            - return_content: text
      debug: True
    
  - name: TSO IEBUPDTE program, add/replace a new dataset member ERASE in sysut1 and store it in sysut2. ERASE content is Hello world!
    zos_mvs_raw:
      program_name: IEBUPDTE
      parms: NEW
      dds:
        - dd_dataset:
            - dd_name: sysut1
            - data_set_name: BJMAXY.CICS.SETUP
            - disposition: old
            - disposition_normal: keep
            - disposition_abnormal: keep
            - return_content: text
        - dd_dataset:
            - dd_name: sysut2
            - data_set_name: BJMAXY.CICS.SETUP
            - disposition: old
            - disposition_normal: keep
            - disposition_abnormal: keep
            - return_content: text
        - dd_input:
            - dd_name: sysin
            - dd_content:
                - "./        ADD   LIST=ALL,NAME=ERASE,LEVEL=01,SOURCE=0"
                - "./     NUMBER   NEW1=10,INCR=10"
                - "Hello world! "
                - "./      ENDUP   "
            - return_content: text
        - dd_dataset:
            - dd_name: sysprint
            - data_set_name: BJMAXY.NOEXIST.DS
      debug: True    
     
  - name: TSO isrsupc program, Compare 2 PDS members olddd and newdd and write the output to outdd.
    zos_mvs_raw:
        program_name: ISRSUPC
        parms: DELTAL,LINECMP
        dds:
          - dd_dataset:
              - dd_name: newdd
              - data_set_name: BJMAXY.MVSUTIL.PYTHON.MVSCMD.A
              - disposition: old
              - disposition_normal: keep
              - disposition_abnormal: keep
              - return_content: text
          - dd_dataset:
              - dd_name: olddd
              - data_set_name: BJMAXY.MVSUTIL.PYTHON.MVSCMD.B
              - disposition: old
              - disposition_normal: keep
              - disposition_abnormal: keep
              - return_content: text
          - dd_dataset:
              - dd_name: sysin
              - data_set_name: BJMAXY.MVSUTIL.PYTHON.MVSCMD.OPT
              - disposition: old
              - disposition_normal: keep
              - disposition_abnormal: keep
              - return_content: text
          - dd_dataset:
              - dd_name: outdd
              - data_set_name: BJMAXY.MVSUTIL.PYTHON.MVSCMD.RESULT
              - disposition: old
              - disposition_normal: keep
              - disposition_abnormal: keep
              - return_content: text
          - dd_dataset:
              - dd_name: sysprint
              - data_set_name: BJMAXY.MVSUTIL.PYTHON.MVSCMD.RESULT2
              - disposition: old
              - disposition_normal: keep
              - disposition_abnormal: keep
              - return_content: text

     
EXAMPLE RESULTS:
"msg": "    
    "changed": true,
    "ddnames": [
        {
            "byte_count": "748",
            "content": "TEST                                                                            ",
            "dataset": "TESTER.MVSUTIL.PYTHON.MVSCMD.A",
            "ddname": "newdd",
            "record_count": 1
        },
        {
            "byte_count": "748",
            "content": "TEST                                                                            ",
            "dataset": "TESTER.MVSUTIL.PYTHON.MVSCMD.B",
            "ddname": "olddd",
            "record_count": 1
        },
        {
            "byte_count": "748",
            "content": "   CMPCOLM 1:72                                                                 ",
            "dataset": "TESTER.MVSUTIL.PYTHON.MVSCMD.OPT",
            "ddname": "sysin",
            "record_count": 1
        },
        {
            "byte_count": "3400",
            "content": "
                       ISRSUPC   -   MVS/PDF FILE/LINE/WORD/BYTE/SFOR COMPARE UTILITY- ISPF FOR z/OS         2020/02/25   3.36    PAGE     1
                        NEW: TESTER.MVSUTIL.PYTHON.MVSCMD.A                          OLD: TESTER.MVSUTIL.PYTHON.MVSCMD.B                       
                                                                                                                       
                                            LINE COMPARE SUMMARY AND STATISTICS                                                             
                                                                                                                       
                                                                                                                       
                                                                                                                       
                            1 NUMBER OF LINE MATCHES               0  TOTAL CHANGES (PAIRED+NONPAIRED CHNG)                                 
                            0 REFORMATTED LINES                    0  PAIRED CHANGES (REFM+PAIRED INS/DEL)                                  
                            0 NEW FILE LINE INSERTIONS             0  NON-PAIRED INSERTS                                                    
                            0 OLD FILE LINE DELETIONS              0  NON-PAIRED DELETES                                                    
                            1 NEW FILE LINES PROCESSED                                                                                      
                            1 OLD FILE LINES PROCESSED                                                                                      
                                                                                                                       
                    LISTING-TYPE = DELTA      COMPARE-COLUMNS =    1:72        LONGEST-LINE = 80                                           
                    PROCESS OPTIONS USED: NONE                                                                                             
                                                                                                                       
                    THE FOLLOWING PROCESS STATEMENTS (USING COLUMNS 1:72) WERE PROCESSED:                                                  
                            CMPCOLM 1:72                                                                                                     
                     " 
            "dataset": "TESTER.MVSUTIL.PYTHON.MVSCMD.RESULT",
            "ddname": "outdd",
            "record_count": 20
        },
        {
            "byte_count": "0",
            "content": "",
            "dataset": "TESTER.MVSUTIL.PYTHON.MVSCMD.RESULT2",
            "ddname": "sysprint",
            "record_count": 1
        }
    ],
    "ret_code": {
        "code": 0,
        "msg": 0,
        "msg_code": 0,
        "msg_txt": "THE z/OS PROGRAM EXECUTION SUCCEED.",
    }
"

"msg" : "
    "changed": true,
    "ddnames": [
        {
            "byte_count": "748",
            "content": "  LISTCAT ENT('TESTER.HILL3')                                                   ",
            "dataset": "TESTER.P3621680.T0979893.C0000000",
            "ddname": "sysin",
            "record_count": 1
        },
        {
            "byte_count": "2006",
            "content": "
                        1IDCAMS  SYSTEM SERVICES                                           TIME: 04:04:12        02/25/20     PAGE      1 
                        0                                                                                                                 
                        LISTCAT ENT('TESTER.HILL3')                                                                                    
                        0NONVSAM ------- TESTER.HILL3                                                                                     
                              IN-CAT --- ICFCAT.SYSPLEX2.CATALOGB                                                                         
                        1IDCAMS  SYSTEM SERVICES                                           TIME: 04:04:12        02/25/20     PAGE      2 
                        0         THE NUMBER OF ENTRIES PROCESSED WAS:                                                                    
                                            AIX -------------------0                                                                      
                                            ALIAS -----------------0                                                                      
                                            CLUSTER ---------------0                                                                      
                                            DATA ------------------0                                                                      
                                            GDG -------------------0                                                                      
                                            INDEX -----------------0                                                                      
                                            NONVSAM ---------------1                                                                      
                                            PAGESPACE -------------0                                                                      
                                            PATH ------------------0                                                                      
                                            SPACE -----------------0                                                                      
                                            USERCATALOG -----------0                                                                      
                                            TAPELIBRARY -----------0                                                                      
                                            TAPEVOLUME ------------0                                                                      
                                            TOTAL -----------------1                                                                      
                        0         THE NUMBER OF PROTECTED ENTRIES SUPPRESSED WAS 0                                                        
                        0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 0                                                        
                        0                                                                                                                 
                        0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 0                                                
            " 
            "dataset": "TESTER.MVSUTIL.PYTHON.MVSCMD.AUTH.OUT",
            "ddname": "sysprint",
            "record_count": 25
        }
    ], 
    "ret_code": {
        "code": 0,
        "msg": 0,
        "msg_code": 0,
        "msg_txt": "THE z/OS PROGRAM EXECUTION SUCCEED."
    }
"
"""

from ansible.module_utils.basic import *
from zoautil_py import MVSCmd, Datasets
import re

MVSCMD = "mvscmd"
MVSCMD_AUTH = "mvscmdauth"

class DDs:
    dds_count = 0
    return_content = None

    def __init__(self, dds_name):
        self.dds_name = dds_name
        DDs.dds_count += 1

    def __init__(self, dds_name, return_content):
        self.dds_name = dds_name
        DDs.dds_count += 1
        DDs.return_content = return_content


def run_mvs_program(program, auth, parms, dds, verbose, debug, module):
    mvscmd_suffix_script = ''' --pgm='''+program

    if parms != None :
        mvscmd_suffix_script = mvscmd_suffix_script+''' --args=\"'''+parms+'''\"'''

    for item in dds:
        dd_name = item.get('ddName')
        dataset = item.get('dataset')
        mvscmd_suffix_script = mvscmd_suffix_script +''' --'''+dd_name+'''='''+dataset

    if verbose:
        mvscmd_suffix_script = mvscmd_suffix_script + ''' --verbose=''' + str(verbose)

    if debug:
        mvscmd_suffix_script = mvscmd_suffix_script + ''' --debug=''' + str(debug)

    mvscmd_command_auth = MVSCMD_AUTH + mvscmd_suffix_script
    mvscmd_command = MVSCMD + mvscmd_suffix_script

    try:
        if auth:
            rc, stdout, stderr = module.run_command(mvscmd_command_auth, use_unsafe_shell=True)
        else:
            rc, stdout, stderr = module.run_command(mvscmd_command, use_unsafe_shell=True)

    except Exception as e:
        raise ZOSRawError(e)
    return (stdout, stderr, rc)


def delete_data_sets(data_sets):
    for data_set in data_sets:
        Datasets.delete(data_set)


def parse_dds(dds,stdout):
    ddnames = []

    for item in dds:
        if item['dataset'] == 'stdout':
            content = stdout
            ddname = {
                'ddname': item['ddName'],
                'dataset': item['dataset'],
                'content': content,
                'record_count': len(re.split(r'\n*', content)),  # the lines of the content
                'byte_count': content.__sizeof__(),  # the bytes of the content
            }
            ddnames.append(ddname)
        elif item['dataset'] == 'dummy':
            content = ""
            ddname = {
                'ddname': item['ddName'],
                'dataset': item['dataset'],
                'content': content,
                'record_count': '0',
                'byte_count': '0',
            }
            ddnames.append(ddname)
        else:
            ddinfo = re.split(r',*', item['dataset'])
            datasets = re.split(r':*', ddinfo[0])
            for i in datasets:
                content = Datasets.read(i)
                dataset_info = Datasets.list(i, verbose=True)
                if content == None:
                    content = ""
                if dataset_info == None:
                    raise ZOSRawError("No datasets "+i+" is found.")
                ddname = {
                    'ddname': item['ddName'],
                    'dataset': i,
                    'content': content,
                    'record_count': len(re.split(r'\n', content)),
                    'byte_count': re.split(r'[\s]\s*', dataset_info)[6]  # In the position 6, it's used bytes.
                }
                ddnames.append(ddname)
    return ddnames


def run_module():

    dd_dataset = dict(
        dd_name=dict(type='str', required=True),
        data_set_name=dict(type='str', required=True),
        disposition=dict(type='str', required=True),
        disposition_normal=dict(type='str', required=True),
        disposition_abnormal=dict(type='str', required=True),
        space_type=dict(type='str', required=True),
        space_primary=dict(type='str', required=True),
        space_secondary=dict(type='str', required=True),
        volume=dict(type='str', required=True),
        sms_management_class=dict(type='str', required=True),
        sms_storage_class=dict(type='str', required=True),
        sms_data_class=dict(type='str', required=True),
        block_size=dict(type='str', required=True),
        data_set_key_label=dict(type='str', required=True),
        data_set_type=dict(type='str', required=True),
        encryption_key_1=dict(type='str', required=True),
        encryption_key_2=dict(type='str', required=True),
        key_length=dict(type='str', required=True),
        record_length=dict(type='str', required=True),
        record_format=dict(type='str', required=True),
        return_content=dict(type='str', required=False, default='None'),
    )

    dd_input = dict(
        dd_name=dict(type='str', required=True),
        dd_content=dict(type='raw', required=True),
        return_content=dict(type='str', required=False, default='None'),
    )

    dd_uss = dict(
        dd_name=dict(type='str', required=True),
        path=dict(type='str', required=True),
        path_disposition_normal=dict(type='str', required=True),
        path_disposition_abnormal=dict(type='str', required=True),
        path_mode=dict(type='str', required=True),
        path_access_group=dict(type='str', required=True, default='read_write'),
        path_status_group=dict(type='list', elements='str', required=True),
        file_data=dict(type='str', required=True),
        return_content=dict(type='str', required=False, default='None'),
    )

    dd_sysout = dict(
        dd_name=dict(type='str', required=True),
        return_content=dict(type='str', required=False, default='None'),
        sysout_class=dict(type='str', required=False, default='*'),
    )

    dd_dummy = dict(
        dd_name=dict(type='str', required=True),
    )
    module_args = dict(
        program_name=dict(type='str', required=True),
        auth=dict(type='bool', required=False, default=False),
        parms=dict(type='str', required=False),
        dds=dict(type='list', elements='dict', required=False),
        verbose=dict(type='bool', required=False),
        debug=dict(type='bool', required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    result = dict(
        changed=False,
        ddnames='',
        ret_code='',
    )
    hlq = Datasets.hlq()
    temp_dds = []

    if module.params.get("program_name") == None:
        module.fail_json(msg='THE z/OS PROGRAM CAN NOT BE EMPTY.', **result)

    try:


        result["original_message"] = module.params


    except ZOSRawError as e:
        module.fail_json(msg="ZOSRawError :"+str(e), **result)
    except Exception as e:
        module.fail_json(msg="Exception :"+str(e), **result)
    finally:
        delete_data_sets(temp_dds)

    result['changed'] = True
    module.exit_json(**result)

class Error(Exception):
    pass

class ZOSRawError(Error):
    def __init__(self, program):
        self.msg = 'An error occurred during execution of z/OS program {}.'.format(program)


def main():
    run_module()


if __name__ == '__main__':
    main()
