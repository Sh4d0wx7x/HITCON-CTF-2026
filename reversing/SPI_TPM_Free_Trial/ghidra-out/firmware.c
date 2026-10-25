INFO  Using log config file: jar:file:/usr/share/ghidra/Ghidra/Framework/Generic/lib/Generic.jar!/generic.log4j.xml (LoggingInitialization)  
INFO  Using log file: /tmp/ghidra-config/sh4d0w-ghidra/ghidra_12.1.3_DEV/application.log (LoggingInitialization)  
INFO  Loading user preferences: /tmp/ghidra-config/sh4d0w-ghidra/ghidra_12.1.3_DEV/preferences (Preferences)  
INFO  Loading previous preferences: /tmp/ghidra-config/sh4d0w-ghidra/ghidra_12.1.1_DEV/preferences (Preferences)  
INFO  Searching for classes... (ClassSearcher)  
INFO  Class search complete (3115 ms) (ClassSearcher)  
INFO  Initializing SSL Context (DefaultSSLContextInitializer)  
INFO  Initializing Random Number Generator... (SecureRandomFactory)  
INFO  Random Number Generator initialization complete: NativePRNGNonBlocking (SecureRandomFactory)  
INFO  Trust manager disabled, cacerts have not been set (DefaultTrustManagerFactory)  
INFO  Starting cache cleanup: /var/tmp/sh4d0w-ghidra/fscache2 (FileCacheMaintenanceDaemon)  
INFO  Finished cache cleanup, estimated storage used: 0 (FileCacheMaintenanceDaemon)  
INFO  Headless startup complete (7868 ms) (AnalyzeHeadless)  
INFO  Class searcher loaded 59 extension points (20 false positives) (ClassSearcher)  
INFO  HEADLESS Script Paths:
    /usr/share/ghidra/Ghidra/Processors/8051/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/DecompilerDependent/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/GnuDemangler/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/BytePatterns/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/FileFormats/ghidra_scripts
    /home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/tools
    /usr/share/ghidra/Ghidra/Features/Base/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/PDB/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/WildcardAssembler/ghidra_scripts
    /usr/share/ghidra/Ghidra/Processors/Atmel/ghidra_scripts
    /usr/share/ghidra/Ghidra/Processors/JVM/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/SwiftDemangler/ghidra_scripts
    /usr/share/ghidra/Ghidra/Processors/DATA/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/SystemEmulation/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/BSim/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/PyGhidra/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/Decompiler/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/MicrosoftCodeAnalyzer/ghidra_scripts
    /usr/share/ghidra/Ghidra/Debug/Debugger-rmi-trace/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/FunctionID/ghidra_scripts
    /usr/share/ghidra/Ghidra/Features/VersionTracking/ghidra_scripts
    /usr/share/ghidra/Ghidra/Debug/Debugger/ghidra_scripts
    /usr/share/ghidra/Ghidra/Processors/PIC/ghidra_scripts (HeadlessAnalyzer)  
INFO  HEADLESS: execution starts (HeadlessAnalyzer)  
INFO  Creating temporary project: /tmp/spitpm-ghidra/fwproj (HeadlessAnalyzer)  
INFO  Creating project: /tmp/spitpm-ghidra/fwproj (DefaultProject)  
INFO  REPORT: Processing input files:  (HeadlessAnalyzer)  
INFO       project: /tmp/spitpm-ghidra/fwproj (HeadlessAnalyzer)  
INFO  IMPORTING: file:///home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so (HeadlessAnalyzer)  
INFO  Using Loader: Executable and Linking Format (ELF) (ProgramLoader)  
INFO  Using Language/Compiler: x86:LE:64:default:gcc (ProgramLoader)  
INFO  Using Library Search Path: [., /bin, /lib, /lib64, /lib/x86_64-linux-gnu, /lib/aarch64-linux-gnu, /usr/bin, /usr/lib, /usr/X11R6/bin, /usr/X11R6/lib, /usr/java/packages/lib, /usr/lib/x86_64-linux-gnu/jni, /usr/lib/x86_64-linux-gnu, /usr/lib/jni] (ProgramLoader)  
INFO  Additional info:
Loading file:///home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so?MD5=baee7059fa016edd902d553cc886d4dd...
Setting block .init_array to read-only
Setting block .fini_array to read-only
Setting block .data.rel.ro to read-only
Setting block .dynamic to read-only
------------------------------------------------

Linking the External Programs of 'libspi_tpm_firmware.so' to imported libraries...
  [libc.so.6] -> not found in project
------------------------------------------------

Resolving External Symbols of [/libspi_tpm_firmware.so] - 11 unresolved symbols, no external libraries configured - skipping
 (ProgramLoader)  
INFO  IMPORTING: Loaded 0 additional files (HeadlessAnalyzer)  
INFO  ANALYZING all memory and code: file:///home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so (HeadlessAnalyzer)  
INFO  DWARF external debug information found: ExternalDebugInfo [filename=null, crc=0, hash=1bd0bc14406dc25121059370893cd91ec839da39, objectType=DEBUGINFO, extra=null] (ExternalDebugFileSectionProvider)  
INFO  Unable to find DWARF information, skipping DWARF analysis (DWARFAnalyzer)  
INFO  hit non-returning function, restarting decompiler switch analyzer later (DecompilerSwitchAnalyzer)  
WARN  Decompiling 00101100, pcode error at 00107010: Unable to disassemble EXTERNAL block location: 00107010 (DecompileCallback)  
WARN  Decompiling 00101130, pcode error at 00107058: Unable to disassemble EXTERNAL block location: 00107058 (DecompileCallback)  
INFO  Packed database cache: /var/tmp/sh4d0w-ghidra/packed-db-cache (PackedDatabaseCache)  
INFO  Applied data type archive: generic_clib_64 (ApplyDataArchiveAnalyzer)  
INFO  -----------------------------------------------------
    ASCII Strings                              0.936 secs
    Apply Data Archives                        1.184 secs
    Call Convention ID                         0.004 secs
    Call-Fixup Installer                       0.010 secs
    Create Address Tables                      0.036 secs
    Create Address Tables - One Time           0.004 secs
    Create Function                            0.048 secs
    DWARF                                      0.051 secs
    Data Reference                             0.029 secs
    Decompiler Switch Analysis                 0.133 secs
    Decompiler Switch Analysis - One Time      2.253 secs
    Demangler GNU                              0.139 secs
    Disassemble Entry Points                   2.143 secs
    ELF Scalar Operand References              0.167 secs
    Embedded Media                             0.010 secs
    External Entry References                  0.000 secs
    Function ID                                0.763 secs
    Function Start Pre Search                  0.030 secs
    Function Start Search                      0.094 secs
    Function Start Search After Code           0.013 secs
    Function Start Search After Data           0.008 secs
    GCC Exception Handlers                     0.482 secs
    Non-Returning Functions - Discovered       0.036 secs
    Non-Returning Functions - Known            0.017 secs
    Reference                                  0.054 secs
    Shared Return Calls                        0.048 secs
    Stack                                      0.674 secs
    Subroutine References                      0.027 secs
    Subroutine References - One Time           0.000 secs
    x86 Constant Reference Analyzer            0.929 secs
-----------------------------------------------------
     Total Time   10 secs
-----------------------------------------------------
 (AutoAnalysisManager)  
INFO  REPORT: Analysis succeeded for file: file:///home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so (HeadlessAnalyzer)  
INFO  REPORT: Execute script: DecompileAll.java  (HeadlessAnalyzer)  
INFO  SCRIPT: /home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/tools/DecompileAll.java (HeadlessAnalyzer)  
INFO  DecompileAll.java> 
/* ===== _DT_INIT @ 00101000 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void _DT_INIT(void)

{
  if (PTR___gmon_start___00105fd8 != (undefined *)0x0) {
    (*(code *)PTR___gmon_start___00105fd8)();
  }
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101020 @ 00101020 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_00101020(void)

{
  (*(code *)PTR_00105f78)();
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101100 @ 00101100 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
/* WARNING: Removing unreachable block (ram,0x00101113) */
/* WARNING: Removing unreachable block (ram,0x0010111f) */

void FUN_00101100(void)

{
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101130 @ 00101130 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
/* WARNING: Removing unreachable block (ram,0x00101154) */
/* WARNING: Removing unreachable block (ram,0x00101160) */

void FUN_00101130(void)

{
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== _FINI_0 @ 00101170 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void _FINI_0(void)

{
  if (DAT_00106008 == '\0') {
    if (PTR___cxa_finalize_00105fe8 != (undefined *)0x0) {
      (*(code *)PTR___cxa_finalize_00105fe8)(PTR_LOOP_00106000);
    }
    FUN_00101100();
    DAT_00106008 = 1;
    return;
  }
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101200 @ 00101200 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_00101200(ulong *param_1,byte param_2)

{
  undefined1 auVar1 [16];
  undefined1 auVar2 [16];
  ushort uVar3;
  ushort uVar4;
  ushort uVar5;
  ushort uVar6;
  short sVar7;
  short sVar8;
  short sVar9;
  short sVar10;
  short sVar11;
  short sVar12;
  short sVar13;
  short sVar14;
  short sVar15;
  byte bVar16;
  byte bVar24;
  char cVar32;
  byte bVar38;
  byte bVar40;
  byte bVar46;
  char cVar54;
  byte bVar55;
  undefined1 auVar56 [15];
  undefined1 auVar57 [15];
  undefined1 auVar58 [15];
  undefined1 auVar59 [15];
  undefined1 auVar60 [14];
  undefined1 auVar61 [14];
  undefined1 auVar62 [14];
  undefined1 auVar63 [14];
  undefined1 auVar64 [14];
  undefined1 auVar65 [14];
  undefined1 auVar66 [15];
  undefined1 auVar67 [15];
  undefined1 auVar68 [15];
  undefined1 auVar69 [15];
  undefined1 auVar70 [14];
  undefined1 auVar71 [14];
  undefined1 auVar72 [14];
  undefined1 auVar73 [13];
  undefined1 auVar74 [13];
  undefined1 auVar75 [13];
  undefined1 auVar76 [13];
  undefined1 auVar77 [13];
  undefined1 auVar78 [13];
  undefined1 auVar79 [14];
  undefined1 auVar80 [15];
  undefined1 auVar81 [15];
  undefined1 auVar82 [15];
  undefined1 auVar83 [15];
  undefined1 auVar84 [15];
  undefined1 auVar85 [15];
  ulong uVar86;
  ushort uVar87;
  undefined1 auVar88 [15];
  unkuint9 Var89;
  undefined1 auVar90 [11];
  undefined1 auVar91 [13];
  undefined1 auVar92 [15];
  unkuint9 Var93;
  undefined1 auVar94 [11];
  undefined1 auVar95 [15];
  undefined1 auVar96 [13];
  undefined1 auVar97 [15];
  undefined1 auVar98 [15];
  undefined1 auVar99 [14];
  undefined1 auVar100 [14];
  undefined1 auVar101 [14];
  undefined1 auVar102 [13];
  undefined1 auVar103 [13];
  undefined1 auVar104 [14];
  undefined3 uVar105;
  undefined3 uVar106;
  undefined3 uVar107;
  undefined3 uVar108;
  undefined1 auVar109 [15];
  undefined1 auVar110 [15];
  undefined1 auVar111 [15];
  undefined1 auVar112 [15];
  undefined1 auVar113 [15];
  undefined1 auVar114 [15];
  undefined1 auVar115 [15];
  undefined5 uVar116;
  undefined5 uVar117;
  undefined5 uVar118;
  undefined5 uVar119;
  undefined1 auVar120 [12];
  undefined8 uVar121;
  undefined1 auVar122 [12];
  undefined8 uVar123;
  undefined1 auVar124 [12];
  undefined1 auVar125 [12];
  undefined1 auVar126 [14];
  undefined1 auVar127 [14];
  undefined1 auVar128 [14];
  undefined1 auVar129 [14];
  uint6 uVar130;
  uint6 uVar131;
  undefined8 *puVar132;
  undefined8 *puVar133;
  uint uVar134;
  uint uVar135;
  uint uVar136;
  uint uVar137;
  uint uVar138;
  uint uVar139;
  uint uVar140;
  uint uVar141;
  uint uVar142;
  uint uVar143;
  byte *pbVar144;
  long in_FS_OFFSET;
  ushort uVar145;
  undefined4 uVar146;
  ushort uVar154;
  ushort uVar155;
  ushort uVar156;
  ushort uVar157;
  ushort uVar158;
  ushort uVar159;
  undefined1 auVar152 [16];
  ushort uVar160;
  ushort uVar161;
  ushort uVar166;
  ushort uVar167;
  ushort uVar168;
  ushort uVar169;
  ushort uVar170;
  undefined1 auVar162 [12];
  ushort uVar171;
  ushort uVar172;
  ushort uVar173;
  undefined4 uVar174;
  ushort uVar186;
  ushort uVar187;
  ushort uVar188;
  ushort uVar189;
  ushort uVar190;
  undefined1 auVar180 [16];
  ushort uVar185;
  ushort uVar191;
  undefined1 auVar182 [16];
  undefined1 auVar183 [16];
  undefined1 auVar184 [16];
  undefined1 auVar192 [16];
  undefined1 auVar193 [16];
  undefined1 auVar194 [16];
  undefined1 auVar195 [16];
  undefined1 auVar196 [16];
  undefined1 auVar197 [16];
  undefined1 auVar198 [16];
  undefined1 auVar199 [16];
  ushort uVar200;
  ushort uVar206;
  ushort uVar207;
  ushort uVar208;
  ushort uVar209;
  ushort uVar210;
  undefined1 auVar201 [12];
  ushort uVar211;
  ushort uVar212;
  undefined1 auVar205 [16];
  undefined1 auVar213 [16];
  undefined1 auVar214 [16];
  undefined1 auVar215 [16];
  undefined1 auVar216 [16];
  ushort uVar217;
  ushort uVar219;
  ushort uVar220;
  ushort uVar221;
  ushort uVar222;
  ushort uVar223;
  ushort uVar224;
  ushort uVar225;
  undefined1 auVar218 [16];
  ushort uVar226;
  ushort uVar227;
  ushort uVar228;
  ushort uVar229;
  ushort uVar230;
  ushort uVar231;
  ushort uVar232;
  ushort uVar233;
  uint local_e4;
  uint local_e0;
  uint local_dc;
  uint local_d8;
  undefined1 local_c8 [16];
  undefined1 local_b8 [16];
  undefined1 local_a8 [16];
  undefined1 local_98 [16];
  undefined8 local_88;
  undefined8 uStack_80;
  uint local_78;
  uint uStack_74;
  uint uStack_70;
  uint uStack_6c;
  uint local_68;
  uint uStack_64;
  uint uStack_60;
  uint uStack_5c;
  uint local_58;
  uint uStack_54;
  uint uStack_50;
  uint uStack_4c;
  undefined8 local_48;
  long local_40;
  char cVar17;
  char cVar18;
  char cVar19;
  char cVar20;
  char cVar21;
  char cVar22;
  char cVar23;
  char cVar25;
  char cVar26;
  char cVar27;
  char cVar28;
  char cVar29;
  char cVar30;
  char cVar31;
  byte bVar33;
  char cVar34;
  char cVar35;
  char cVar36;
  char cVar37;
  byte bVar39;
  char cVar41;
  char cVar42;
  char cVar43;
  char cVar44;
  char cVar45;
  char cVar47;
  char cVar48;
  char cVar49;
  char cVar50;
  char cVar51;
  char cVar52;
  char cVar53;
  undefined6 uVar147;
  undefined8 uVar148;
  undefined1 auVar149 [12];
  undefined1 auVar150 [14];
  undefined1 auVar151 [15];
  undefined1 auVar153 [16];
  undefined1 auVar163 [14];
  undefined1 auVar164 [15];
  undefined1 auVar165 [16];
  undefined6 uVar175;
  undefined8 uVar176;
  undefined1 auVar177 [12];
  undefined1 auVar178 [14];
  undefined1 auVar179 [15];
  undefined1 auVar181 [16];
  undefined1 auVar202 [14];
  undefined1 auVar203 [15];
  undefined1 auVar204 [16];
  
  auVar182._8_2_ = 0xff;
  auVar182._0_8_ = 0xff00ff00ff00ff;
  auVar182._10_2_ = 0xff;
  auVar182._12_2_ = 0xff;
  auVar182._14_2_ = 0xff;
  pbVar144 = &DAT_00104080;
  local_d8 = -(uint)param_2 ^ 0x1f83d9ab;
  uStack_5c = 0xa54ff53a;
  uStack_64 = 0xbb67ae85;
  local_68 = 0x6a09e667;
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  auVar194 = *(undefined1 (*) [16])(param_1 + 5);
  auVar196 = *(undefined1 (*) [16])(param_1 + 7);
  auVar1 = *(undefined1 (*) [16])(param_1 + 9);
  auVar2 = *(undefined1 (*) [16])(param_1 + 0xb);
  auVar180 = auVar182 & auVar196;
  auVar152 = auVar182 & auVar194;
  uVar3 = auVar152._0_2_;
  uVar200 = auVar152._2_2_;
  bVar16 = (uVar200 != 0) * (uVar200 < 0x100) * auVar152[2] - (0xff < uVar200);
  uVar200 = auVar152._4_2_;
  uVar4 = auVar152._6_2_;
  cVar17 = (uVar4 != 0) * (uVar4 < 0x100) * auVar152[6] - (0xff < uVar4);
  uVar146 = CONCAT13(cVar17,CONCAT12((uVar200 != 0) * (uVar200 < 0x100) * auVar152[4] -
                                     (0xff < uVar200),
                                     CONCAT11(bVar16,(uVar3 != 0) * (uVar3 < 0x100) * auVar152[0] -
                                                     (0xff < uVar3))));
  sVar7 = auVar152._8_2_;
  sVar8 = auVar152._10_2_;
  cVar18 = (0 < sVar8) * (sVar8 < 0x100) * auVar152[10] - (0xff < sVar8);
  uVar147 = CONCAT15(cVar18,CONCAT14((0 < sVar7) * (sVar7 < 0x100) * auVar152[8] - (0xff < sVar7),
                                     uVar146));
  sVar7 = auVar152._12_2_;
  sVar8 = auVar152._14_2_;
  cVar19 = (0 < sVar8) * (sVar8 < 0x100) * auVar152[0xe] - (0xff < sVar8);
  uVar148 = CONCAT17(cVar19,CONCAT16((0 < sVar7) * (sVar7 < 0x100) * auVar152[0xc] - (0xff < sVar7),
                                     uVar147));
  uVar3 = auVar180._0_2_;
  uVar200 = auVar180._2_2_;
  cVar20 = (uVar200 != 0) * (uVar200 < 0x100) * auVar180[2] - (0xff < uVar200);
  auVar149._0_10_ =
       CONCAT19(cVar20,CONCAT18((uVar3 != 0) * (uVar3 < 0x100) * auVar180[0] - (0xff < uVar3),
                                uVar148));
  uVar3 = auVar180._4_2_;
  auVar149[10] = (uVar3 != 0) * (uVar3 < 0x100) * auVar180[4] - (0xff < uVar3);
  uVar3 = auVar180._6_2_;
  cVar21 = (uVar3 != 0) * (uVar3 < 0x100) * auVar180[6] - (0xff < uVar3);
  auVar149[0xb] = cVar21;
  sVar7 = auVar180._8_2_;
  auVar150[0xc] = (0 < sVar7) * (sVar7 < 0x100) * auVar180[8] - (0xff < sVar7);
  auVar150._0_12_ = auVar149;
  sVar7 = auVar180._10_2_;
  cVar22 = (0 < sVar7) * (sVar7 < 0x100) * auVar180[10] - (0xff < sVar7);
  auVar150[0xd] = cVar22;
  sVar7 = auVar180._12_2_;
  auVar151[0xe] = (0 < sVar7) * (sVar7 < 0x100) * auVar180[0xc] - (0xff < sVar7);
  auVar151._0_14_ = auVar150;
  sVar7 = auVar180._14_2_;
  cVar23 = (0 < sVar7) * (sVar7 < 0x100) * auVar180[0xe] - (0xff < sVar7);
  auVar153[0xf] = cVar23;
  auVar153._0_15_ = auVar151;
  auVar192 = auVar182 & auVar2;
  auVar180 = auVar182 & auVar1;
  uVar161 = auVar194._0_2_ >> 8;
  uVar166 = auVar194._2_2_ >> 8;
  uVar167 = auVar194._4_2_ >> 8;
  uVar168 = auVar194._6_2_ >> 8;
  uVar169 = auVar194._8_2_ >> 8;
  uVar170 = auVar194._10_2_ >> 8;
  uVar171 = auVar194._12_2_ >> 8;
  uVar172 = auVar194._14_2_ >> 8;
  auVar152[0xf] = 0;
  auVar152._0_15_ = auVar151;
  auVar152 = auVar182 & auVar152;
  local_58 = (uint)param_1[4] ^ 0x510e527f;
  uVar3 = auVar180._0_2_;
  uVar200 = auVar180._2_2_;
  bVar24 = (uVar200 != 0) * (uVar200 < 0x100) * auVar180[2] - (0xff < uVar200);
  uVar200 = auVar180._4_2_;
  uVar4 = auVar180._6_2_;
  cVar25 = (uVar4 != 0) * (uVar4 < 0x100) * auVar180[6] - (0xff < uVar4);
  uVar174 = CONCAT13(cVar25,CONCAT12((uVar200 != 0) * (uVar200 < 0x100) * auVar180[4] -
                                     (0xff < uVar200),
                                     CONCAT11(bVar24,(uVar3 != 0) * (uVar3 < 0x100) * auVar180[0] -
                                                     (0xff < uVar3))));
  sVar7 = auVar180._8_2_;
  sVar8 = auVar180._10_2_;
  cVar26 = (0 < sVar8) * (sVar8 < 0x100) * auVar180[10] - (0xff < sVar8);
  uVar175 = CONCAT15(cVar26,CONCAT14((0 < sVar7) * (sVar7 < 0x100) * auVar180[8] - (0xff < sVar7),
                                     uVar174));
  sVar7 = auVar180._12_2_;
  sVar8 = auVar180._14_2_;
  cVar27 = (0 < sVar8) * (sVar8 < 0x100) * auVar180[0xe] - (0xff < sVar8);
  uVar176 = CONCAT17(cVar27,CONCAT16((0 < sVar7) * (sVar7 < 0x100) * auVar180[0xc] - (0xff < sVar7),
                                     uVar175));
  uVar3 = auVar192._0_2_;
  uVar200 = auVar192._2_2_;
  cVar28 = (uVar200 != 0) * (uVar200 < 0x100) * auVar192[2] - (0xff < uVar200);
  auVar177._0_10_ =
       CONCAT19(cVar28,CONCAT18((uVar3 != 0) * (uVar3 < 0x100) * auVar192[0] - (0xff < uVar3),
                                uVar176));
  uVar3 = auVar192._4_2_;
  auVar177[10] = (uVar3 != 0) * (uVar3 < 0x100) * auVar192[4] - (0xff < uVar3);
  uVar3 = auVar192._6_2_;
  cVar29 = (uVar3 != 0) * (uVar3 < 0x100) * auVar192[6] - (0xff < uVar3);
  auVar177[0xb] = cVar29;
  sVar7 = auVar192._8_2_;
  auVar178[0xc] = (0 < sVar7) * (sVar7 < 0x100) * auVar192[8] - (0xff < sVar7);
  auVar178._0_12_ = auVar177;
  sVar7 = auVar192._10_2_;
  cVar30 = (0 < sVar7) * (sVar7 < 0x100) * auVar192[10] - (0xff < sVar7);
  auVar178[0xd] = cVar30;
  sVar7 = auVar192._12_2_;
  auVar179[0xe] = (0 < sVar7) * (sVar7 < 0x100) * auVar192[0xc] - (0xff < sVar7);
  auVar179._0_14_ = auVar178;
  sVar7 = auVar192._14_2_;
  cVar31 = (0 < sVar7) * (sVar7 < 0x100) * auVar192[0xe] - (0xff < sVar7);
  auVar181[0xf] = cVar31;
  auVar181._0_15_ = auVar179;
  uStack_54 = *(uint *)((long)param_1 + 0x24) ^ 0x9b05688c;
  uVar217 = auVar2._0_2_ >> 8;
  uVar219 = auVar2._2_2_ >> 8;
  uVar220 = auVar2._4_2_ >> 8;
  uVar221 = auVar2._6_2_ >> 8;
  uVar222 = auVar2._8_2_ >> 8;
  uVar223 = auVar2._10_2_ >> 8;
  uVar224 = auVar2._12_2_ >> 8;
  uVar225 = auVar2._14_2_ >> 8;
  uVar145 = (ushort)bVar16;
  uVar154 = (ushort)((uint)uVar146 >> 0x18);
  uVar155 = (ushort)((uint6)uVar147 >> 0x28);
  uVar156 = (ushort)((ulong)uVar148 >> 0x38);
  uVar157 = (ushort)((unkuint10)auVar149._0_10_ >> 0x48);
  uVar158 = auVar149._10_2_ >> 8;
  uVar159 = auVar150._12_2_ >> 8;
  uVar160 = auVar153._14_2_ >> 8;
  auVar180[0xf] = 0;
  auVar180._0_15_ = auVar179;
  auVar180 = auVar182 & auVar180;
  uVar226 = auVar196._0_2_ >> 8;
  uVar227 = auVar196._2_2_ >> 8;
  uVar228 = auVar196._4_2_ >> 8;
  uVar229 = auVar196._6_2_ >> 8;
  uVar230 = auVar196._8_2_ >> 8;
  uVar231 = auVar196._10_2_ >> 8;
  uVar232 = auVar196._12_2_ >> 8;
  uVar233 = auVar196._14_2_ >> 8;
  uVar173 = (ushort)bVar24;
  uVar185 = (ushort)((uint)uVar174 >> 0x18);
  uVar186 = (ushort)((uint6)uVar175 >> 0x28);
  uVar187 = (ushort)((ulong)uVar176 >> 0x38);
  uVar188 = (ushort)((unkuint10)auVar177._0_10_ >> 0x48);
  uVar189 = auVar177._10_2_ >> 8;
  uVar190 = auVar178._12_2_ >> 8;
  uVar191 = auVar181._14_2_ >> 8;
  uVar3 = auVar152._0_2_;
  uVar4 = auVar152._2_2_;
  uVar5 = auVar152._4_2_;
  uVar6 = auVar152._6_2_;
  sVar7 = auVar152._8_2_;
  sVar9 = auVar152._10_2_;
  sVar11 = auVar152._12_2_;
  sVar8 = auVar152._14_2_;
  cVar32 = (0 < sVar8) * (sVar8 < 0x100) * auVar152[0xe] - (0xff < sVar8);
  uVar200 = auVar180._0_2_;
  bVar33 = (uVar200 != 0) * (uVar200 < 0x100) * auVar180[0] - (0xff < uVar200);
  uVar87 = CONCAT11(bVar33,cVar32);
  uVar200 = auVar180._2_2_;
  cVar34 = (uVar200 != 0) * (uVar200 < 0x100) * auVar180[2] - (0xff < uVar200);
  uVar105 = CONCAT12(cVar34,uVar87);
  uVar200 = auVar180._4_2_;
  cVar35 = (uVar200 != 0) * (uVar200 < 0x100) * auVar180[4] - (0xff < uVar200);
  uVar137 = CONCAT13(cVar35,uVar105);
  uVar200 = auVar180._6_2_;
  cVar36 = (uVar200 != 0) * (uVar200 < 0x100) * auVar180[6] - (0xff < uVar200);
  uVar116 = CONCAT14(cVar36,uVar137);
  sVar8 = auVar180._8_2_;
  cVar37 = (0 < sVar8) * (sVar8 < 0x100) * auVar180[8] - (0xff < sVar8);
  auVar129[5] = cVar37;
  auVar129._0_5_ = uVar116;
  sVar8 = auVar180._10_2_;
  sVar10 = auVar180._12_2_;
  sVar12 = auVar180._14_2_;
  uVar200 = auVar1._0_2_ >> 8;
  uVar206 = auVar1._2_2_ >> 8;
  uVar207 = auVar1._4_2_ >> 8;
  uVar208 = auVar1._6_2_ >> 8;
  uVar209 = auVar1._8_2_ >> 8;
  uVar210 = auVar1._10_2_ >> 8;
  uVar211 = auVar1._12_2_ >> 8;
  uVar212 = auVar1._14_2_ >> 8;
  cVar23 = (uVar160 != 0) * (uVar160 < 0x100) * cVar23 - (0xff < uVar160);
  bVar24 = (uVar173 != 0) * (uVar173 < 0x100) * bVar24 - (0xff < uVar173);
  uVar173 = CONCAT11(bVar24,cVar23);
  cVar25 = (uVar185 != 0) * (uVar185 < 0x100) * cVar25 - (0xff < uVar185);
  uVar106 = CONCAT12(cVar25,uVar173);
  bVar38 = (uVar186 != 0) * (uVar186 < 0x100) * cVar26 - (0xff < uVar186);
  uVar142 = CONCAT13(bVar38,uVar106);
  cVar27 = (uVar187 != 0) * (uVar187 < 0x100) * cVar27 - (0xff < uVar187);
  uVar117 = CONCAT14(cVar27,uVar142);
  bVar39 = (uVar188 != 0) * (uVar188 < 0x100) * cVar28 - (0xff < uVar188);
  auVar126[5] = bVar39;
  auVar126._0_5_ = uVar117;
  bVar40 = (uVar166 != 0) * (uVar166 < 0x100) * auVar194[3] - (0xff < uVar166);
  cVar28 = (uVar168 != 0) * (uVar168 < 0x100) * auVar194[7] - (0xff < uVar168);
  uVar146 = CONCAT13(cVar28,CONCAT12((uVar167 != 0) * (uVar167 < 0x100) * auVar194[5] -
                                     (0xff < uVar167),
                                     CONCAT11(bVar40,(uVar161 != 0) * (uVar161 < 0x100) *
                                                     auVar194[1] - (0xff < uVar161))));
  cVar41 = (uVar170 != 0) * (uVar170 < 0x100) * auVar194[0xb] - (0xff < uVar170);
  uVar147 = CONCAT15(cVar41,CONCAT14((uVar169 != 0) * (uVar169 < 0x100) * auVar194[9] -
                                     (0xff < uVar169),uVar146));
  cVar42 = (uVar172 != 0) * (uVar172 < 0x100) * auVar194[0xf] - (0xff < uVar172);
  uVar148 = CONCAT17(cVar42,CONCAT16((uVar171 != 0) * (uVar171 < 0x100) * auVar194[0xd] -
                                     (0xff < uVar171),uVar147));
  cVar43 = (uVar227 != 0) * (uVar227 < 0x100) * auVar196[3] - (0xff < uVar227);
  auVar162._0_10_ =
       CONCAT19(cVar43,CONCAT18((uVar226 != 0) * (uVar226 < 0x100) * auVar196[1] - (0xff < uVar226),
                                uVar148));
  auVar162[10] = (uVar228 != 0) * (uVar228 < 0x100) * auVar196[5] - (0xff < uVar228);
  cVar44 = (uVar229 != 0) * (uVar229 < 0x100) * auVar196[7] - (0xff < uVar229);
  auVar162[0xb] = cVar44;
  auVar163[0xc] = (uVar230 != 0) * (uVar230 < 0x100) * auVar196[9] - (0xff < uVar230);
  auVar163._0_12_ = auVar162;
  cVar45 = (uVar231 != 0) * (uVar231 < 0x100) * auVar196[0xb] - (0xff < uVar231);
  auVar163[0xd] = cVar45;
  auVar164[0xe] = (uVar232 != 0) * (uVar232 < 0x100) * auVar196[0xd] - (0xff < uVar232);
  auVar164._0_14_ = auVar163;
  cVar26 = (uVar233 != 0) * (uVar233 < 0x100) * auVar196[0xf] - (0xff < uVar233);
  auVar165[0xf] = cVar26;
  auVar165._0_15_ = auVar164;
  bVar46 = (uVar206 != 0) * (uVar206 < 0x100) * auVar1[3] - (0xff < uVar206);
  cVar47 = (uVar208 != 0) * (uVar208 < 0x100) * auVar1[7] - (0xff < uVar208);
  uVar174 = CONCAT13(cVar47,CONCAT12((uVar207 != 0) * (uVar207 < 0x100) * auVar1[5] -
                                     (0xff < uVar207),
                                     CONCAT11(bVar46,(uVar200 != 0) * (uVar200 < 0x100) * auVar1[1]
                                                     - (0xff < uVar200))));
  cVar48 = (uVar210 != 0) * (uVar210 < 0x100) * auVar1[0xb] - (0xff < uVar210);
  uVar175 = CONCAT15(cVar48,CONCAT14((uVar209 != 0) * (uVar209 < 0x100) * auVar1[9] -
                                     (0xff < uVar209),uVar174));
  cVar49 = (uVar212 != 0) * (uVar212 < 0x100) * auVar1[0xf] - (0xff < uVar212);
  uVar176 = CONCAT17(cVar49,CONCAT16((uVar211 != 0) * (uVar211 < 0x100) * auVar1[0xd] -
                                     (0xff < uVar211),uVar175));
  cVar50 = (uVar219 != 0) * (uVar219 < 0x100) * auVar2[3] - (0xff < uVar219);
  auVar201._0_10_ =
       CONCAT19(cVar50,CONCAT18((uVar217 != 0) * (uVar217 < 0x100) * auVar2[1] - (0xff < uVar217),
                                uVar176));
  auVar201[10] = (uVar220 != 0) * (uVar220 < 0x100) * auVar2[5] - (0xff < uVar220);
  cVar51 = (uVar221 != 0) * (uVar221 < 0x100) * auVar2[7] - (0xff < uVar221);
  auVar201[0xb] = cVar51;
  auVar202[0xc] = (uVar222 != 0) * (uVar222 < 0x100) * auVar2[9] - (0xff < uVar222);
  auVar202._0_12_ = auVar201;
  cVar52 = (uVar223 != 0) * (uVar223 < 0x100) * auVar2[0xb] - (0xff < uVar223);
  auVar202[0xd] = cVar52;
  auVar203[0xe] = (uVar224 != 0) * (uVar224 < 0x100) * auVar2[0xd] - (0xff < uVar224);
  auVar203._0_14_ = auVar202;
  cVar53 = (uVar225 != 0) * (uVar225 < 0x100) * auVar2[0xf] - (0xff < uVar225);
  auVar204[0xf] = cVar53;
  auVar204._0_15_ = auVar203;
  auVar194[0xf] = 0;
  auVar194._0_15_ = auVar203;
  auVar194 = auVar182 & auVar194;
  auVar196[0xf] = 0;
  auVar196._0_15_ = auVar164;
  auVar182 = auVar182 & auVar196;
  auVar215[1] = 0;
  auVar215[0] = bVar33;
  auVar215[2] = cVar34;
  auVar215[3] = 0;
  auVar215[4] = cVar35;
  auVar215[5] = 0;
  auVar215[6] = cVar36;
  auVar215[7] = 0;
  auVar215[8] = cVar37;
  auVar215[9] = 0;
  auVar215[10] = (0 < sVar8) * (sVar8 < 0x100) * auVar180[10] - (0xff < sVar8);
  auVar215[0xb] = 0;
  auVar215[0xc] = (0 < sVar10) * (sVar10 < 0x100) * auVar180[0xc] - (0xff < sVar10);
  auVar215[0xd] = 0;
  auVar215[0xe] = (0 < sVar12) * (sVar12 < 0x100) * auVar180[0xe] - (0xff < sVar12);
  auVar215[0xf] = 0;
  uVar200 = auVar182._0_2_;
  uVar160 = auVar182._2_2_;
  uVar161 = auVar182._4_2_;
  uVar166 = auVar182._6_2_;
  sVar8 = auVar182._8_2_;
  sVar10 = auVar182._10_2_;
  sVar12 = auVar182._12_2_;
  sVar13 = auVar182._14_2_;
  cVar34 = (0 < sVar13) * (sVar13 < 0x100) * auVar182[0xe] - (0xff < sVar13);
  uVar167 = auVar194._0_2_;
  bVar33 = (uVar167 != 0) * (uVar167 < 0x100) * auVar194[0] - (0xff < uVar167);
  uVar168 = CONCAT11(bVar33,cVar34);
  uVar167 = auVar194._2_2_;
  cVar35 = (uVar167 != 0) * (uVar167 < 0x100) * auVar194[2] - (0xff < uVar167);
  uVar107 = CONCAT12(cVar35,uVar168);
  uVar167 = auVar194._4_2_;
  cVar36 = (uVar167 != 0) * (uVar167 < 0x100) * auVar194[4] - (0xff < uVar167);
  uVar135 = CONCAT13(cVar36,uVar107);
  uVar167 = auVar194._6_2_;
  cVar37 = (uVar167 != 0) * (uVar167 < 0x100) * auVar194[6] - (0xff < uVar167);
  uVar118 = CONCAT14(cVar37,uVar135);
  sVar13 = auVar194._8_2_;
  cVar54 = (0 < sVar13) * (sVar13 < 0x100) * auVar194[8] - (0xff < sVar13);
  auVar128[5] = cVar54;
  auVar128._0_5_ = uVar118;
  sVar13 = auVar194._10_2_;
  sVar14 = auVar194._12_2_;
  sVar15 = auVar194._14_2_;
  uVar188 = (ushort)bVar46;
  uVar206 = (ushort)((uint)uVar174 >> 0x18);
  uVar207 = (ushort)((uint6)uVar175 >> 0x28);
  uVar208 = (ushort)((ulong)uVar176 >> 0x38);
  uVar209 = (ushort)((unkuint10)auVar201._0_10_ >> 0x48);
  uVar210 = auVar201._10_2_ >> 8;
  uVar211 = auVar202._12_2_ >> 8;
  uVar212 = auVar204._14_2_ >> 8;
  uVar169 = (ushort)bVar40;
  uVar170 = (ushort)((uint)uVar146 >> 0x18);
  uVar171 = (ushort)((uint6)uVar147 >> 0x28);
  uVar172 = (ushort)((ulong)uVar148 >> 0x38);
  uVar185 = (ushort)((unkuint10)auVar162._0_10_ >> 0x48);
  uVar186 = auVar162._10_2_ >> 8;
  uVar187 = auVar163._12_2_ >> 8;
  uVar167 = auVar165._14_2_ >> 8;
  auVar183[1] = 0;
  auVar183[0] = bVar33;
  auVar183[2] = cVar35;
  auVar183[3] = 0;
  auVar183[4] = cVar36;
  auVar183[5] = 0;
  auVar183[6] = cVar37;
  auVar183[7] = 0;
  auVar183[8] = cVar54;
  auVar183[9] = 0;
  auVar183[10] = (0 < sVar13) * (sVar13 < 0x100) * auVar194[10] - (0xff < sVar13);
  auVar183[0xb] = 0;
  auVar183[0xc] = (0 < sVar14) * (sVar14 < 0x100) * auVar194[0xc] - (0xff < sVar14);
  auVar183[0xd] = 0;
  auVar183[0xe] = (0 < sVar15) * (sVar15 < 0x100) * auVar194[0xe] - (0xff < sVar15);
  auVar183[0xf] = 0;
  cVar26 = (uVar167 != 0) * (uVar167 < 0x100) * cVar26 - (0xff < uVar167);
  bVar33 = (uVar188 != 0) * (uVar188 < 0x100) * bVar46 - (0xff < uVar188);
  uVar167 = CONCAT11(bVar33,cVar26);
  cVar35 = (uVar206 != 0) * (uVar206 < 0x100) * cVar47 - (0xff < uVar206);
  uVar108 = CONCAT12(cVar35,uVar167);
  bVar46 = (uVar207 != 0) * (uVar207 < 0x100) * cVar48 - (0xff < uVar207);
  uVar134 = CONCAT13(bVar46,uVar108);
  cVar36 = (uVar208 != 0) * (uVar208 < 0x100) * cVar49 - (0xff < uVar208);
  uVar119 = CONCAT14(cVar36,uVar134);
  bVar55 = (uVar209 != 0) * (uVar209 < 0x100) * cVar50 - (0xff < uVar209);
  auVar127[5] = bVar55;
  auVar127._0_5_ = uVar119;
  auVar194 = psllw(auVar183,8);
  auVar126._6_8_ = 0;
  auVar56[0xe] = cVar23;
  auVar56._0_14_ = auVar126 << 0x38;
  auVar120._4_8_ = 0;
  auVar120._0_4_ = uVar142;
  auVar66._12_3_ =
       (int3)(CONCAT26(auVar56._13_2_,
                       CONCAT15((uVar159 != 0) * (uVar159 < 0x100) * cVar22 - (0xff < uVar159),
                                uVar117)) >> 0x28);
  auVar66._0_12_ = auVar120 << 0x38;
  uVar142 = auVar66._11_4_;
  uVar121 = CONCAT44(uVar142,CONCAT13((uVar158 != 0) * (uVar158 < 0x100) * cVar21 - (0xff < uVar158)
                                      ,uVar106));
  auVar80._10_5_ = (int5)((ulong)uVar121 >> 0x18);
  auVar80._0_10_ = (unkuint10)uVar173 << 0x38;
  uVar148 = CONCAT62(auVar80._9_6_,
                     CONCAT11((uVar157 != 0) * (uVar157 < 0x100) * cVar20 - (0xff < uVar157),cVar23)
                    );
  auVar88._7_8_ = 0;
  auVar88._0_7_ = (uint7)((ulong)uVar148 >> 8);
  Var89 = CONCAT81(SUB158(auVar88 << 0x40,7),
                   (uVar156 != 0) * (uVar156 < 0x100) * cVar19 - (0xff < uVar156));
  auVar109._9_6_ = 0;
  auVar109._0_9_ = Var89;
  auVar90._1_10_ = SUB1510(auVar109 << 0x30,5);
  auVar90[0] = (uVar155 != 0) * (uVar155 < 0x100) * cVar18 - (0xff < uVar155);
  auVar110._11_4_ = 0;
  auVar110._0_11_ = auVar90;
  auVar91._1_12_ = SUB1512(auVar110 << 0x20,3);
  auVar91[0] = (uVar154 != 0) * (uVar154 < 0x100) * cVar17 - (0xff < uVar154);
  auVar84[1] = 0;
  auVar84[0] = (uVar145 != 0) * (uVar145 < 0x100) * bVar16 - (0xff < uVar145);
  auVar84._2_13_ = auVar91;
  auVar194 = auVar194 | auVar215;
  auVar127._6_8_ = 0;
  auVar57[0xe] = cVar26;
  auVar57._0_14_ = auVar127 << 0x38;
  auVar122._4_8_ = 0;
  auVar122._0_4_ = uVar134;
  auVar67._12_3_ =
       (int3)(CONCAT26(auVar57._13_2_,
                       CONCAT15((uVar187 != 0) * (uVar187 < 0x100) * cVar45 - (0xff < uVar187),
                                uVar119)) >> 0x28);
  auVar67._0_12_ = auVar122 << 0x38;
  uVar134 = auVar67._11_4_;
  uVar123 = CONCAT44(uVar134,CONCAT13((uVar186 != 0) * (uVar186 < 0x100) * cVar44 - (0xff < uVar186)
                                      ,uVar108));
  auVar81._10_5_ = (int5)((ulong)uVar123 >> 0x18);
  auVar81._0_10_ = (unkuint10)uVar167 << 0x38;
  uVar176 = CONCAT62(auVar81._9_6_,
                     CONCAT11((uVar185 != 0) * (uVar185 < 0x100) * cVar43 - (0xff < uVar185),cVar26)
                    );
  auVar92._7_8_ = 0;
  auVar92._0_7_ = (uint7)((ulong)uVar176 >> 8);
  Var93 = CONCAT81(SUB158(auVar92 << 0x40,7),
                   (uVar172 != 0) * (uVar172 < 0x100) * cVar42 - (0xff < uVar172));
  auVar111._9_6_ = 0;
  auVar111._0_9_ = Var93;
  auVar94._1_10_ = SUB1510(auVar111 << 0x30,5);
  auVar94[0] = (uVar171 != 0) * (uVar171 < 0x100) * cVar41 - (0xff < uVar171);
  auVar95._11_4_ = 0;
  auVar95._0_11_ = auVar94;
  auVar96._1_12_ = SUB1512(auVar95 << 0x20,3);
  auVar96[0] = (uVar170 != 0) * (uVar170 < 0x100) * cVar28 - (0xff < uVar170);
  auVar85[1] = 0;
  auVar85[0] = (uVar169 != 0) * (uVar169 < 0x100) * bVar40 - (0xff < uVar169);
  auVar85._2_13_ = auVar96;
  auVar128._6_8_ = 0;
  auVar58[0xe] = cVar34;
  auVar58._0_14_ = auVar128 << 0x38;
  auVar124._4_8_ = 0;
  auVar124._0_4_ = uVar135;
  auVar68._12_3_ =
       (int3)(CONCAT26(auVar58._13_2_,
                       CONCAT15((0 < sVar12) * (sVar12 < 0x100) * auVar182[0xc] - (0xff < sVar12),
                                uVar118)) >> 0x28);
  auVar68._0_12_ = auVar124 << 0x38;
  auVar82._10_5_ =
       (int5)(CONCAT44(auVar68._11_4_,
                       CONCAT13((0 < sVar10) * (sVar10 < 0x100) * auVar182[10] - (0xff < sVar10),
                                uVar107)) >> 0x18);
  auVar82._0_10_ = (unkuint10)uVar168 << 0x38;
  auVar97._7_8_ = 0;
  auVar97._0_7_ =
       (uint7)(CONCAT62(auVar82._9_6_,
                        CONCAT11((0 < sVar8) * (sVar8 < 0x100) * auVar182[8] - (0xff < sVar8),cVar34
                                )) >> 8);
  auVar112._1_8_ = SUB158(auVar97 << 0x40,7);
  auVar112[0] = (uVar166 != 0) * (uVar166 < 0x100) * auVar182[6] - (0xff < uVar166);
  auVar112._9_6_ = 0;
  auVar113._1_10_ = SUB1510(auVar112 << 0x30,5);
  auVar113[0] = (uVar161 != 0) * (uVar161 < 0x100) * auVar182[4] - (0xff < uVar161);
  auVar113._11_4_ = 0;
  auVar195._3_12_ = SUB1512(auVar113 << 0x20,3);
  auVar195[2] = (uVar160 != 0) * (uVar160 < 0x100) * auVar182[2] - (0xff < uVar160);
  auVar195[1] = 0;
  auVar195[0] = (uVar200 != 0) * (uVar200 < 0x100) * auVar182[0] - (0xff < uVar200);
  auVar195[0xf] = 0;
  auVar129._6_8_ = 0;
  auVar59[0xe] = cVar32;
  auVar59._0_14_ = auVar129 << 0x38;
  auVar125._4_8_ = 0;
  auVar125._0_4_ = uVar137;
  auVar69._12_3_ =
       (int3)(CONCAT26(auVar59._13_2_,
                       CONCAT15((0 < sVar11) * (sVar11 < 0x100) * auVar152[0xc] - (0xff < sVar11),
                                uVar116)) >> 0x28);
  auVar69._0_12_ = auVar125 << 0x38;
  auVar83._10_5_ =
       (int5)(CONCAT44(auVar69._11_4_,
                       CONCAT13((0 < sVar9) * (sVar9 < 0x100) * auVar152[10] - (0xff < sVar9),
                                uVar105)) >> 0x18);
  auVar83._0_10_ = (unkuint10)uVar87 << 0x38;
  auVar98._7_8_ = 0;
  auVar98._0_7_ =
       (uint7)(CONCAT62(auVar83._9_6_,
                        CONCAT11((0 < sVar7) * (sVar7 < 0x100) * auVar152[8] - (0xff < sVar7),cVar32
                                )) >> 8);
  auVar114._1_8_ = SUB158(auVar98 << 0x40,7);
  auVar114[0] = (uVar6 != 0) * (uVar6 < 0x100) * auVar152[6] - (0xff < uVar6);
  auVar114._9_6_ = 0;
  auVar115._1_10_ = SUB1510(auVar114 << 0x30,5);
  auVar115[0] = (uVar5 != 0) * (uVar5 < 0x100) * auVar152[4] - (0xff < uVar5);
  auVar115._11_4_ = 0;
  auVar218._3_12_ = SUB1512(auVar115 << 0x20,3);
  auVar218[2] = (uVar4 != 0) * (uVar4 < 0x100) * auVar152[2] - (0xff < uVar4);
  auVar218[1] = 0;
  auVar218[0] = (uVar3 != 0) * (uVar3 < 0x100) * auVar152[0] - (0xff < uVar3);
  auVar218[0xf] = 0;
  auVar196 = psllw(auVar195,8);
  auVar60._10_2_ = 0;
  auVar60._0_10_ = auVar84._0_10_;
  auVar60._12_2_ = (short)Var89;
  uVar130 = CONCAT42(auVar60._10_4_,auVar90._0_2_);
  auVar99._6_8_ = 0;
  auVar99._0_6_ = uVar130;
  auVar70._4_2_ = auVar91._0_2_;
  auVar70._0_4_ = auVar84._0_4_;
  auVar70._6_8_ = SUB148(auVar99 << 0x40,6);
  auVar61._10_2_ = 0;
  auVar61._0_10_ = auVar85._0_10_;
  auVar61._12_2_ = (short)Var93;
  uVar131 = CONCAT42(auVar61._10_4_,auVar94._0_2_);
  auVar100._6_8_ = 0;
  auVar100._0_6_ = uVar131;
  auVar71._4_2_ = auVar96._0_2_;
  auVar71._0_4_ = auVar85._0_4_;
  auVar71._6_8_ = SUB148(auVar100 << 0x40,6);
  auVar196 = auVar196 | auVar218;
  auVar213._0_4_ = auVar85._0_4_ << 0x18;
  auVar213._4_4_ = auVar71._4_4_ << 0x18;
  auVar213._8_4_ = (int)uVar131 << 0x18;
  auVar213._12_4_ = (auVar61._10_4_ >> 0x10) << 0x18;
  uVar137 = CONCAT13(0,CONCAT12(cVar25,(ushort)bVar24));
  auVar205._0_4_ = auVar84._0_4_ << 0x10;
  auVar205._4_4_ = auVar70._4_4_ << 0x10;
  auVar205._8_4_ = (int)uVar130 << 0x10;
  auVar205._12_4_ = auVar60._10_4_ & 0xffff0000;
  auVar1._2_4_ = (uint)(ushort)((ulong)uVar121 >> 0x18) << 0x10;
  auVar1._0_2_ = (short)((ulong)uVar148 >> 8);
  auVar1._6_4_ = (uVar142 >> 8) << 0x10;
  auVar1._10_4_ = (uVar142 >> 0x18) << 0x10;
  auVar1._14_2_ = 0;
  uVar142 = CONCAT13(0,CONCAT12(cVar35,(ushort)bVar33));
  auVar216._0_4_ = (uint)(ushort)((ulong)uVar176 >> 8) << 0x18;
  auVar216._4_4_ = (uint)(ushort)((ulong)uVar123 >> 0x18) << 0x18;
  auVar216._8_4_ = (uVar134 >> 8) << 0x18;
  auVar216._12_4_ = uVar134 & 0xff000000;
  auVar197._2_2_ = 0;
  auVar197._0_2_ = auVar196._8_2_;
  auVar197._4_2_ = auVar196._10_2_;
  auVar197._6_2_ = 0;
  auVar197._8_2_ = auVar196._12_2_;
  auVar197._10_2_ = 0;
  auVar197._12_2_ = auVar196._14_2_;
  auVar197._14_2_ = 0;
  auVar62._10_2_ = 0;
  auVar62._0_10_ = auVar196._0_10_;
  auVar62._12_2_ = auVar196._6_2_;
  auVar64._8_2_ = auVar196._4_2_;
  auVar64._0_8_ = auVar196._0_8_;
  auVar64._10_4_ = auVar62._10_4_;
  auVar101._6_8_ = 0;
  auVar101._0_6_ = auVar64._8_6_;
  auVar72._4_2_ = auVar196._2_2_;
  auVar72._0_4_ = auVar196._0_4_;
  auVar72._6_8_ = SUB148(auVar101 << 0x40,6);
  auVar214._0_4_ = auVar196._0_4_ & 0xffff;
  auVar214._4_10_ = auVar72._4_10_;
  auVar214._14_2_ = 0;
  local_b8 = auVar1 << 0x10 | auVar216 | auVar197;
  auVar73[0xc] = cVar36;
  auVar73._0_12_ = ZEXT112(bVar55) << 0x40;
  auVar74._10_3_ = auVar73._10_3_;
  auVar74._0_10_ = (unkuint10)bVar46 << 0x40;
  auVar102._5_8_ = 0;
  auVar102._0_5_ = auVar74._8_5_;
  auVar75[4] = cVar35;
  auVar75._0_4_ = uVar142;
  auVar75[5] = 0;
  auVar75._6_7_ = SUB137(auVar102 << 0x40,6);
  auVar76[0xc] = cVar27;
  auVar76._0_12_ = ZEXT112(bVar39) << 0x40;
  auVar77._10_3_ = auVar76._10_3_;
  auVar77._0_10_ = (unkuint10)bVar38 << 0x40;
  auVar103._5_8_ = 0;
  auVar103._0_5_ = auVar77._8_5_;
  auVar78[4] = cVar25;
  auVar78._0_4_ = uVar137;
  auVar78[5] = 0;
  auVar78._6_7_ = SUB137(auVar103 << 0x40,6);
  auVar198._0_4_ = uVar142 << 0x18;
  auVar198._4_4_ = auVar75._4_4_ << 0x18;
  auVar198._8_4_ = auVar74._8_4_ << 0x18;
  auVar198._12_4_ = (uint)(uint3)(auVar73._10_3_ >> 0x10) << 0x18;
  auVar2._1_4_ = (uint)(byte)((uVar210 != 0) * (uVar210 < 0x100) * cVar51 - (0xff < uVar210)) <<
                 0x18;
  auVar2[0] = bVar55;
  auVar2._5_4_ = (uint)(byte)((uVar211 != 0) * (uVar211 < 0x100) * cVar52 - (0xff < uVar211)) <<
                 0x18;
  auVar2._9_4_ = (uint)(byte)((uVar212 != 0) * (uVar212 < 0x100) * cVar53 - (0xff < uVar212)) <<
                 0x18;
  auVar2._13_3_ = 0;
  auVar193._0_4_ = uVar137 << 0x10;
  auVar193._4_4_ = auVar78._4_4_ << 0x10;
  auVar193._8_4_ = auVar77._8_4_ << 0x10;
  auVar193._12_4_ = (uint)(uint3)(auVar76._10_3_ >> 0x10) << 0x10;
  local_c8 = auVar205 | auVar213 | auVar214;
  auVar192._0_4_ = (uint)bVar39 << 0x10;
  auVar192._4_4_ =
       (uint)(byte)((uVar189 != 0) * (uVar189 < 0x100) * cVar29 - (0xff < uVar189)) << 0x10;
  auVar192._8_4_ =
       (uint)(byte)((uVar190 != 0) * (uVar190 < 0x100) * cVar30 - (0xff < uVar190)) << 0x10;
  auVar192._12_4_ =
       (uint)(byte)((uVar191 != 0) * (uVar191 < 0x100) * cVar31 - (0xff < uVar191)) << 0x10;
  auVar184._2_2_ = 0;
  auVar184._0_2_ = auVar194._8_2_;
  auVar184._4_2_ = auVar194._10_2_;
  auVar184._6_2_ = 0;
  auVar184._8_2_ = auVar194._12_2_;
  auVar184._10_2_ = 0;
  auVar184._12_2_ = auVar194._14_2_;
  auVar184._14_2_ = 0;
  uVar86 = *param_1;
  uStack_80 = param_1[1];
  auVar63._10_2_ = 0;
  auVar63._0_10_ = auVar194._0_10_;
  auVar63._12_2_ = auVar194._6_2_;
  auVar65._8_2_ = auVar194._4_2_;
  auVar65._0_8_ = auVar194._0_8_;
  auVar65._10_4_ = auVar63._10_4_;
  auVar104._6_8_ = 0;
  auVar104._0_6_ = auVar65._8_6_;
  auVar79._4_2_ = auVar194._2_2_;
  auVar79._0_4_ = auVar194._0_4_;
  auVar79._6_8_ = SUB148(auVar104 << 0x40,6);
  auVar199._0_4_ = auVar194._0_4_ & 0xffff;
  auVar199._4_10_ = auVar79._4_10_;
  auVar199._14_2_ = 0;
  local_78 = (uint)param_1[2];
  uStack_74 = *(uint *)((long)param_1 + 0x14);
  local_dc = (uint)param_1[3];
  local_e4 = *(uint *)((long)param_1 + 0x1c);
  local_88 = uVar86;
  local_88._4_4_ = (uint)(uVar86 >> 0x20);
  uVar142 = (uint)uVar86;
  uStack_70 = local_dc;
  uStack_6c = local_e4;
  local_a8 = auVar193 | auVar198 | auVar199;
  local_98 = auVar184 | auVar192 | auVar2 << 0x18;
  uStack_80._4_4_ = (uint)(uStack_80 >> 0x20);
  local_e0 = 0x5be0cd19;
  uStack_60 = 0x3c6ef372;
  do {
    uVar142 = *(int *)(local_c8 + (ulong)*pbVar144 * 4) + local_78 + uVar142;
    local_58 = local_58 ^ uVar142;
    uVar134 = local_58 << 0x10 | local_58 >> 0x10;
    local_68 = local_68 + uVar134;
    local_78 = local_78 ^ local_68;
    uVar137 = local_78 >> 0xc | local_78 << 0x14;
    uVar142 = *(int *)(local_c8 + (ulong)pbVar144[1] * 4) + uVar137 + uVar142;
    uVar134 = uVar134 ^ uVar142;
    uVar135 = uVar134 >> 8 | uVar134 << 0x18;
    local_68 = local_68 + uVar135;
    uVar137 = uVar137 ^ local_68;
    uVar138 = uVar137 >> 7 | uVar137 << 0x19;
    local_88._4_4_ = *(int *)(local_c8 + (ulong)pbVar144[2] * 4) + uStack_74 + local_88._4_4_;
    uStack_54 = uStack_54 ^ local_88._4_4_;
    uVar134 = uStack_54 << 0x10 | uStack_54 >> 0x10;
    uStack_64 = uStack_64 + uVar134;
    uStack_74 = uStack_74 ^ uStack_64;
    uVar137 = uStack_74 >> 0xc | uStack_74 << 0x14;
    local_88._4_4_ = *(int *)(local_c8 + (ulong)pbVar144[3] * 4) + uVar137 + local_88._4_4_;
    uVar134 = uVar134 ^ local_88._4_4_;
    uVar136 = uVar134 >> 8 | uVar134 << 0x18;
    uStack_64 = uStack_64 + uVar136;
    uVar137 = uVar137 ^ uStack_64;
    uVar143 = uVar137 >> 7 | uVar137 << 0x19;
    uStack_80._0_4_ = *(int *)(local_c8 + (ulong)pbVar144[4] * 4) + local_dc + (uint)uStack_80;
    local_d8 = local_d8 ^ (uint)uStack_80;
    uVar134 = local_d8 << 0x10 | local_d8 >> 0x10;
    uStack_60 = uVar134 + uStack_60;
    local_dc = local_dc ^ uStack_60;
    uVar139 = local_dc >> 0xc | local_dc << 0x14;
    uStack_80._0_4_ = *(int *)(local_c8 + (ulong)pbVar144[5] * 4) + uVar139 + (uint)uStack_80;
    uVar134 = uVar134 ^ (uint)uStack_80;
    uVar137 = uVar134 >> 8 | uVar134 << 0x18;
    uStack_60 = uStack_60 + uVar137;
    uVar139 = uVar139 ^ uStack_60;
    uStack_80._4_4_ = local_e4 + *(int *)(local_c8 + (ulong)pbVar144[6] * 4) + uStack_80._4_4_;
    uVar140 = uVar139 >> 7 | uVar139 << 0x19;
    local_e0 = local_e0 ^ uStack_80._4_4_;
    uVar139 = local_e0 << 0x10 | local_e0 >> 0x10;
    uStack_5c = uStack_5c + uVar139;
    local_e4 = local_e4 ^ uStack_5c;
    uVar134 = local_e4 >> 0xc | local_e4 << 0x14;
    uStack_80._4_4_ = *(int *)(local_c8 + (ulong)pbVar144[7] * 4) + uVar134 + uStack_80._4_4_;
    uVar139 = uVar139 ^ uStack_80._4_4_;
    uVar139 = uVar139 >> 8 | uVar139 << 0x18;
    uVar142 = uVar142 + *(int *)(local_c8 + (ulong)pbVar144[8] * 4) + uVar143;
    uStack_5c = uStack_5c + uVar139;
    uVar139 = uVar139 ^ uVar142;
    uVar134 = uVar134 ^ uStack_5c;
    uVar141 = uVar139 << 0x10 | uVar139 >> 0x10;
    uVar139 = uVar134 >> 7 | uVar134 << 0x19;
    uStack_60 = uStack_60 + uVar141;
    uVar143 = uVar143 ^ uStack_60;
    uVar134 = uVar143 >> 0xc | uVar143 << 0x14;
    uVar142 = uVar142 + *(int *)(local_c8 + (ulong)pbVar144[9] * 4) + uVar134;
    uVar141 = uVar141 ^ uVar142;
    local_e0 = uVar141 >> 8 | uVar141 << 0x18;
    uStack_60 = uStack_60 + local_e0;
    uVar134 = uVar134 ^ uStack_60;
    uStack_74 = uVar134 >> 7 | uVar134 << 0x19;
    uVar141 = local_88._4_4_ + *(int *)(local_c8 + (ulong)pbVar144[10] * 4) + uVar140;
    uVar135 = uVar135 ^ uVar141;
    uVar134 = uVar135 << 0x10 | uVar135 >> 0x10;
    uStack_5c = uStack_5c + uVar134;
    uVar140 = uVar140 ^ uStack_5c;
    uVar135 = uVar140 >> 0xc | uVar140 << 0x14;
    local_88._4_4_ = uVar141 + *(int *)(local_c8 + (ulong)pbVar144[0xb] * 4) + uVar135;
    uVar134 = uVar134 ^ local_88._4_4_;
    local_58 = uVar134 >> 8 | uVar134 << 0x18;
    uStack_5c = uStack_5c + local_58;
    uVar135 = uVar135 ^ uStack_5c;
    local_dc = uVar135 >> 7 | uVar135 << 0x19;
    uVar135 = (uint)uStack_80 + *(int *)(local_c8 + (ulong)pbVar144[0xc] * 4) + uVar139;
    uVar136 = uVar136 ^ uVar135;
    uVar134 = uVar136 << 0x10 | uVar136 >> 0x10;
    local_68 = local_68 + uVar134;
    uVar139 = uVar139 ^ local_68;
    uVar136 = uVar139 >> 0xc | uVar139 << 0x14;
    uStack_80._0_4_ = uVar135 + *(int *)(local_c8 + (ulong)pbVar144[0xd] * 4) + uVar136;
    uVar134 = uVar134 ^ (uint)uStack_80;
    uStack_54 = uVar134 >> 8 | uVar134 << 0x18;
    local_68 = local_68 + uStack_54;
    uVar136 = uVar136 ^ local_68;
    local_e4 = uVar136 >> 7 | uVar136 << 0x19;
    uVar134 = uStack_80._4_4_ + *(int *)(local_c8 + (ulong)pbVar144[0xe] * 4) + uVar138;
    uVar137 = uVar137 ^ uVar134;
    uVar137 = uVar137 << 0x10 | uVar137 >> 0x10;
    uStack_64 = uStack_64 + uVar137;
    uVar138 = uVar138 ^ uStack_64;
    uVar135 = uVar138 >> 0xc | uVar138 << 0x14;
    uStack_80._4_4_ = uVar134 + *(int *)(local_c8 + (ulong)pbVar144[0xf] * 4) + uVar135;
    uVar137 = uVar137 ^ uStack_80._4_4_;
    local_d8 = uVar137 >> 8 | uVar137 << 0x18;
    pbVar144 = pbVar144 + 0x10;
    uStack_64 = uStack_64 + local_d8;
    uVar135 = uVar135 ^ uStack_64;
    local_78 = uVar135 >> 7 | uVar135 << 0x19;
  } while (pbVar144 != &DAT_00104120);
  local_88 = CONCAT44(local_88._4_4_,uVar142);
  *param_1 = CONCAT44(uStack_64,local_68) ^ local_88 ^ *param_1;
  param_1[1] = CONCAT44(uStack_5c,uStack_60) ^ uStack_80 ^ param_1[1];
  param_1[2] = CONCAT44(uStack_74,local_78) ^ CONCAT44(uStack_54,local_58) ^ param_1[2];
  param_1[3] = CONCAT44(local_e4,local_dc) ^ CONCAT44(local_e0,local_d8) ^ param_1[3];
  puVar133 = (undefined8 *)local_c8;
  do {
    puVar132 = (undefined8 *)((long)puVar133 + 1);
    *(undefined1 *)puVar133 = 0;
    puVar133 = puVar132;
  } while (puVar132 != &local_88);
  uStack_70 = local_dc;
  uStack_6c = local_e4;
  uStack_50 = local_d8;
  uStack_4c = local_e0;
  do {
    puVar133 = (undefined8 *)((long)puVar132 + 1);
    *(undefined1 *)puVar132 = 0;
    puVar132 = puVar133;
  } while (puVar133 != &local_48);
  if (local_40 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_001017e0 @ 001017e0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint FUN_001017e0(uint param_1,uint param_2,int param_3,int param_4,char param_5,char param_6)

{
  byte bVar1;
  byte bVar2;
  uint uVar3;
  uint uVar4;
  ushort uVar5;
  int iVar6;
  int iVar7;
  byte bVar8;
  uint uVar9;
  uint *puVar10;
  long in_FS_OFFSET;
  uint uVar14;
  undefined1 auVar11 [16];
  undefined1 auVar12 [16];
  undefined1 auVar13 [16];
  undefined1 auVar15 [16];
  undefined1 auVar16 [16];
  undefined1 auVar18 [16];
  undefined1 local_28 [16];
  uint local_18;
  uint local_14;
  long local_10;
  undefined1 auVar17 [16];
  undefined1 auVar19 [16];
  
  puVar10 = (uint *)local_28;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  uVar4 = param_3 * -0x61c88647 ^ param_2 ^ param_4 * 0x735a2d97 ^
          (-(uint)(param_5 == '\0') & 0xbb03e172) + 0xd1b54a35;
  auVar15._0_4_ = uVar4 + _DAT_00104120;
  auVar15._4_4_ = uVar4 + _UNK_00104124;
  auVar15._8_4_ = uVar4 + _UNK_00104128;
  auVar15._12_4_ = uVar4 + _UNK_0010412c;
  auVar11._0_4_ = auVar15._0_4_ >> 0x10;
  auVar11._4_4_ = auVar15._4_4_ >> 0x10;
  auVar11._8_4_ = auVar15._8_4_ >> 0x10;
  auVar11._12_4_ = auVar15._12_4_ >> 0x10;
  auVar11 = auVar11 ^ auVar15;
  auVar16._0_4_ = auVar11._0_4_ * 0x21f0aaad;
  uVar9 = (uVar4 + 0x1715609d >> 0x10 ^ uVar4 + 0x1715609d) * 0x21f0aaad;
  uVar3 = (uint)((auVar11._0_8_ >> 0x20) * 0x21f0aaad);
  uVar14 = (uint)((auVar11._8_8_ >> 0x20) * 0x21f0aaad);
  auVar17._8_4_ = (uint)((auVar11._8_8_ & 0xffffffff) * 0x21f0aaad);
  auVar17._4_4_ = auVar17._8_4_;
  auVar17._0_4_ = auVar16._0_4_;
  auVar17._12_4_ = uVar14;
  auVar16._8_8_ = auVar17._8_8_;
  auVar16._4_4_ = uVar3;
  auVar12._0_4_ = auVar16._0_4_ >> 0xf;
  auVar12._4_4_ = uVar3 >> 0xf;
  auVar12._8_4_ = auVar17._8_4_ >> 0xf;
  auVar12._12_4_ = uVar14 >> 0xf;
  auVar12 = auVar12 ^ auVar16;
  uVar9 = (uVar9 >> 0xf ^ uVar9) * 0x735a2d97;
  auVar18._0_4_ = auVar12._0_4_ * 0x735a2d97;
  local_18 = uVar9 ^ uVar9 >> 0xf;
  uVar3 = (uint)((auVar12._0_8_ >> 0x20) * 0x735a2d97);
  uVar14 = (uint)((auVar12._8_8_ >> 0x20) * 0x735a2d97);
  auVar19._8_4_ = (uint)((auVar12._8_8_ & 0xffffffff) * 0x735a2d97);
  auVar19._4_4_ = auVar19._8_4_;
  auVar19._0_4_ = auVar18._0_4_;
  auVar19._12_4_ = uVar14;
  auVar18._8_8_ = auVar19._8_8_;
  auVar18._4_4_ = uVar3;
  uVar9 = (uVar4 + 0xb54cda56 >> 0x10 ^ uVar4 + 0xb54cda56) * 0x21f0aaad;
  auVar13._0_4_ = auVar18._0_4_ >> 0xf;
  auVar13._4_4_ = uVar3 >> 0xf;
  auVar13._8_4_ = auVar19._8_4_ >> 0xf;
  auVar13._12_4_ = uVar14 >> 0xf;
  local_28 = auVar13 ^ auVar18;
  uVar9 = (uVar9 >> 0xf ^ uVar9) * 0x735a2d97;
  local_14 = uVar9 ^ uVar9 >> 0xf;
  if (param_6 == '\0') {
    bVar8 = 7;
    uVar3 = param_1 >> 0x10;
    uVar9 = param_1;
    iVar6 = 3;
    do {
      param_1 = uVar3;
      uVar4 = *puVar10;
      puVar10 = puVar10 + 1;
      bVar1 = bVar8 & 0xf;
      iVar7 = iVar6 + 2;
      bVar8 = bVar8 + 1;
      bVar2 = (byte)iVar6 & 0xf;
      uVar5 = (ushort)(uVar4 + param_1);
      uVar3 = (uint)(ushort)((ushort)param_1 << bVar1 | (ushort)param_1 >> 0x10 - bVar1) +
              (uVar4 >> 0x10) ^ (uint)(ushort)(uVar5 << bVar2 | uVar5 >> 0x10 - bVar2) ^ uVar9;
      uVar9 = param_1;
      iVar6 = iVar7;
    } while (iVar7 != 0xf);
  }
  else {
    puVar10 = &local_14;
    uVar9 = param_1 >> 0x10;
    iVar6 = 0xc;
    bVar8 = 0xd;
    do {
      uVar3 = param_1;
      uVar4 = *puVar10;
      iVar7 = iVar6 + -1;
      bVar1 = (byte)iVar6 & 0xf;
      puVar10 = puVar10 + -1;
      uVar5 = (ushort)(uVar4 + uVar3);
      param_1 = (uint)(ushort)((ushort)uVar3 << bVar1 | (ushort)uVar3 >> 0x10 - bVar1) +
                (uVar4 >> 0x10) ^
                (uint)(ushort)(uVar5 << (bVar8 & 0xf) | uVar5 >> 0x10 - (bVar8 & 0xf)) ^ uVar9;
      uVar9 = uVar3;
      iVar6 = iVar7;
      bVar8 = bVar8 - 2;
    } while (iVar7 != 6);
  }
  if (*(long *)(in_FS_OFFSET + 0x28) != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar3 << 0x10 | param_1 & 0xffff;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101a00 @ 00101a00 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined8 FUN_00101a00(void)

{
  return 0x24b8;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101a10 @ 00101a10 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
char * FUN_00101a10(long param_1)

{
  if ((param_1 != 0) && (*(char *)(param_1 + 0x2444) != '\0')) {
    return (char *)(param_1 + 0x2444);
  }
  return "no firmware error";
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101a40 @ 00101a40 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_00101a40(undefined1 *param_1)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  
  if (param_1 != (undefined1 *)0x0) {
    puVar1 = param_1;
    do {
      puVar2 = puVar1 + 1;
      *puVar1 = 0;
      puVar1 = puVar2;
    } while (param_1 + 0x24b0 != puVar2);
  }
  free(param_1);
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101a70 @ 00101a70 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined8 FUN_00101a70(void *param_1,undefined8 *param_2,ulong param_3,undefined8 *param_4)

{
  if (param_4 != (undefined8 *)0x0) {
    *param_4 = 0x24b8;
  }
  if ((param_2 != (undefined8 *)0x0 && 0x24b7 < param_3) && (param_1 != (void *)0x0)) {
    *param_2 = 0x543524657;
    memcpy(param_2 + 1,param_1,0x24b0);
    return 0;
  }
  return 0xffffffff;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101ad0 @ 00101ad0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00101ad0(undefined1 (*param_1) [16])

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  *param_1 = (undefined1  [16])0x0;
  memset(param_1 + 1,0,0x1000);
  memset(param_1 + 0x101,0xff,0x1008);
  uVar2 = _UNK_00104138;
  uVar1 = _DAT_00104130;
  *(undefined8 *)param_1[0x243] = 0;
  *(undefined8 *)param_1[0x242] = uVar1;
  *(undefined8 *)(param_1[0x242] + 8) = uVar2;
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101b20 @ 00101b20 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_00101b20(long param_1,undefined1 param_2,ushort param_3)

{
  int iVar1;
  
  memset((void *)(param_1 + 0x1010),0xff,0x1008);
  iVar1 = *(int *)(param_1 + 0x2434);
  *(ushort *)(param_1 + 0x1012) = param_3;
  *(undefined1 *)(param_1 + 0x1010) = 0xa5;
  *(undefined1 *)(param_1 + 0x1011) = param_2;
  *(undefined4 *)(param_1 + 0x1014) = 0;
  *(uint *)(param_1 + 0x2430) = param_3 + 8;
  if (iVar1 == 0) {
    iVar1 = *(int *)(param_1 + 0x242c) + param_3 + 8;
  }
  *(int *)(param_1 + 0x2424) = iVar1;
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101b90 @ 00101b90 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined8 FUN_00101b90(long param_1,ulong param_2)

{
  long lVar1;
  int *piVar2;
  ulong uVar3;
  
  uVar3 = 0;
  do {
    lVar1 = getrandom(param_1 + uVar3,param_2 - uVar3,0);
    if (lVar1 < 0) {
      piVar2 = __errno_location();
      if (*piVar2 != 4) {
        return 0;
      }
    }
    else {
      if (lVar1 == 0) {
        return 0;
      }
      uVar3 = uVar3 + lVar1;
    }
  } while (uVar3 < param_2);
  return 1;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101bf0 @ 00101bf0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
uint FUN_00101bf0(undefined1 (*param_1) [16])

{
  uint uVar1;
  undefined1 *puVar2;
  undefined1 *puVar3;
  long in_FS_OFFSET;
  undefined1 local_58 [64];
  undefined1 local_18 [8];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  uVar1 = FUN_00101b90(local_58,0x40);
  if ((char)uVar1 != '\0') {
    *param_1 = (undefined1  [16])0x0;
    param_1[1] = (undefined1  [16])0x0;
    param_1[2] = (undefined1  [16])0x0;
    param_1[3] = (undefined1  [16])0x0;
    param_1[4] = (undefined1  [16])0x0;
    param_1[5] = (undefined1  [16])0x0;
    param_1[6] = (undefined1  [16])0x0;
    param_1[7] = (undefined1  [16])0x0;
    FUN_001034a0(param_1 + 1,local_58);
    uVar1 = uVar1 & 0xff;
    puVar2 = local_58;
    do {
      puVar3 = puVar2 + 1;
      *puVar2 = 0;
      puVar2 = puVar3;
    } while (puVar3 != local_18);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar1;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101ca0 @ 00101ca0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_00101ca0(long param_1)

{
  char cVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  long in_FS_OFFSET;
  undefined1 local_24 [4];
  long local_20 [2];
  
  local_20[0] = *(long *)(in_FS_OFFSET + 0x28);
  cVar1 = FUN_00101b90(local_24,4);
  if (cVar1 != '\0') {
    if (local_24 == (undefined1  [4])0x0) {
      local_24 = (undefined1  [4])0x1;
    }
    *(undefined1 (*) [4])(param_1 + 0x243c) = local_24;
    plVar2 = (long *)local_24;
    do {
      plVar3 = (long *)((long)plVar2 + 1);
      *(undefined1 *)plVar2 = 0;
      plVar2 = plVar3;
    } while (plVar3 != local_20);
    lVar4 = param_1 + 0x2020;
    do {
      cVar1 = FUN_00101bf0(lVar4);
      if (cVar1 == '\0') break;
      lVar4 = lVar4 + 0x80;
    } while (lVar4 != param_1 + 0x2420);
  }
  if (local_20[0] != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101d50 @ 00101d50 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined8 FUN_00101d50(uint *param_1,undefined8 *param_2)

{
  char cVar1;
  undefined1 *__ptr;
  undefined1 *puVar2;
  undefined1 *puVar3;
  
  if ((param_2 != (undefined8 *)0x0) && ((param_1 == (uint *)0x0 || (0xb < *param_1)))) {
    *param_2 = 0;
    __ptr = calloc(1,0x24b0);
    if (__ptr != (undefined1 *)0x0) {
      cVar1 = FUN_00101ca0(__ptr);
      if (cVar1 != '\0') {
        FUN_00101ad0(__ptr);
        *param_2 = __ptr;
        return 0;
      }
      puVar2 = __ptr;
      do {
        puVar3 = puVar2 + 1;
        *puVar2 = 0;
        puVar2 = puVar3;
      } while (puVar3 != __ptr + 0x24b0);
      free(__ptr);
    }
    return 0xffffffff;
  }
  return 0xffffffff;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101df0 @ 00101df0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_00101df0(long param_1,void *param_2,ulong param_3)

{
  uint uVar1;
  long lVar2;
  ulong __n;
  
  if (param_3 == 0) {
    return;
  }
  while( true ) {
    while( true ) {
      __n = 0x40 - *(long *)(param_1 + 0x68);
      if (param_3 < __n) {
        __n = param_3;
      }
      param_3 = param_3 - __n;
      memcpy((void *)(param_1 + 0x28 + *(long *)(param_1 + 0x68)),param_2,__n);
      lVar2 = *(long *)(param_1 + 0x68) + __n;
      *(long *)(param_1 + 0x68) = lVar2;
      if (lVar2 != 0x40) break;
      if (param_3 == 0) {
        return;
      }
      uVar1 = *(uint *)(param_1 + 0x20);
      *(uint *)(param_1 + 0x20) = uVar1 + 0x40;
      if (0xffffffbf < uVar1) {
        *(int *)(param_1 + 0x24) = *(int *)(param_1 + 0x24) + 1;
      }
      param_2 = (void *)((long)param_2 + __n);
      FUN_00101200(param_1,0);
      *(undefined8 *)(param_1 + 0x68) = 0;
    }
    if (param_3 == 0) break;
    param_2 = (void *)((long)param_2 + __n);
  }
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00101ea0 @ 00101ea0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00101ea0(long param_1,long param_2,long param_3,undefined4 param_4,void *param_5)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  short sVar5;
  char cVar6;
  char cVar10;
  char cVar18;
  unkbyte10 Var21;
  undefined1 auVar22 [16];
  undefined1 auVar23 [16];
  undefined1 auVar24 [16];
  undefined1 auVar25 [16];
  unkbyte10 Var26;
  ulong uVar27;
  uint uVar28;
  undefined4 uVar29;
  int iVar30;
  undefined8 *puVar31;
  undefined8 *puVar32;
  ulong uVar33;
  ulong *puVar34;
  ulong *puVar35;
  int iVar36;
  long in_FS_OFFSET;
  bool bVar37;
  undefined1 auVar38 [12];
  undefined1 auVar39 [12];
  undefined1 auVar40 [16];
  undefined1 auVar43 [16];
  undefined1 auVar48 [16];
  undefined1 auVar58 [16];
  undefined2 uVar63;
  undefined1 auVar65 [12];
  undefined1 auVar66 [16];
  undefined1 auVar68 [16];
  undefined1 auVar75 [16];
  undefined1 auVar76 [16];
  undefined1 auVar80 [16];
  undefined1 auVar84 [16];
  undefined1 auVar85 [16];
  undefined1 auVar96 [16];
  undefined1 auVar99 [16];
  undefined1 auVar103 [16];
  ushort uVar108;
  ushort uVar111;
  undefined1 auVar109 [16];
  undefined1 auVar110 [16];
  ushort uVar112;
  ushort uVar113;
  ushort uVar114;
  ushort uVar115;
  ushort uVar126;
  ushort uVar127;
  undefined2 uVar128;
  undefined1 auVar116 [16];
  ushort uVar129;
  ushort uVar130;
  ulong local_128;
  undefined8 uStack_120;
  ulong local_118;
  undefined8 uStack_110;
  undefined1 local_108 [16];
  undefined1 local_f8 [16];
  undefined1 local_e8 [16];
  undefined1 local_d8 [16];
  undefined1 local_c8 [16];
  size_t local_b8;
  ulong local_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined1 local_68 [16];
  undefined1 local_58 [16];
  undefined8 local_48;
  long local_40;
  char cVar7;
  char cVar8;
  char cVar9;
  char cVar11;
  char cVar12;
  char cVar13;
  char cVar14;
  char cVar15;
  char cVar16;
  byte bVar17;
  char cVar19;
  char cVar20;
  undefined1 auVar49 [16];
  undefined1 auVar50 [16];
  undefined1 auVar41 [16];
  undefined1 auVar42 [16];
  undefined1 auVar44 [16];
  undefined1 auVar51 [16];
  undefined1 auVar52 [16];
  undefined1 auVar45 [16];
  undefined1 auVar53 [16];
  undefined1 auVar59 [16];
  undefined1 auVar54 [16];
  undefined1 auVar46 [16];
  undefined1 auVar47 [16];
  undefined1 auVar55 [16];
  undefined1 auVar60 [16];
  undefined1 auVar56 [16];
  undefined1 auVar57 [16];
  ushort uVar61;
  undefined8 uVar62;
  undefined3 uVar64;
  undefined1 auVar69 [16];
  undefined1 auVar70 [16];
  undefined1 auVar71 [16];
  undefined1 auVar67 [16];
  undefined1 auVar72 [16];
  undefined1 auVar73 [16];
  undefined1 auVar74 [16];
  undefined1 auVar77 [16];
  undefined1 auVar81 [16];
  undefined1 auVar78 [16];
  undefined1 auVar82 [16];
  undefined1 auVar79 [16];
  undefined1 auVar83 [16];
  undefined1 auVar86 [16];
  undefined1 auVar87 [16];
  undefined1 auVar88 [16];
  undefined1 auVar89 [16];
  undefined1 auVar90 [16];
  undefined1 auVar91 [16];
  undefined1 auVar97 [16];
  undefined1 auVar92 [16];
  undefined1 auVar93 [16];
  undefined1 auVar98 [16];
  undefined1 auVar94 [16];
  undefined1 auVar95 [16];
  undefined1 auVar100 [16];
  undefined1 auVar101 [16];
  undefined1 auVar102 [16];
  undefined1 auVar104 [16];
  undefined1 auVar105 [16];
  undefined1 auVar106 [16];
  ushort uVar107;
  undefined1 auVar117 [16];
  undefined1 auVar118 [16];
  undefined1 auVar119 [16];
  undefined1 auVar120 [16];
  undefined1 auVar121 [16];
  undefined1 auVar122 [16];
  undefined1 auVar123 [16];
  undefined1 auVar124 [16];
  undefined1 auVar125 [16];
  
  iVar2 = *(int *)(param_3 + 0xc);
  uVar3 = *(uint *)(param_3 + 0x14);
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  uVar4 = *(uint *)(param_3 + 8);
  FUN_00103690(param_2 + 0x10,&local_a8);
  local_68 = (undefined1  [16])0x0;
  local_58 = (undefined1  [16])0x0;
  local_108 = (undefined1  [16])0x0;
  local_f8 = (undefined1  [16])0x0;
  local_e8 = (undefined1  [16])0x0;
  local_d8 = (undefined1  [16])0x0;
  local_c8 = (undefined1  [16])0x0;
  local_b8 = 0x10;
  local_128 = _DAT_00104140;
  uStack_120 = _UNK_00104148;
  local_118 = _DAT_00104150;
  uStack_110 = _UNK_00104158;
  local_88 = local_a8;
  uStack_80 = uStack_a0;
  local_78 = local_98;
  uStack_70 = uStack_90;
  FUN_00101df0(&local_128,&local_88,0x40);
  puVar32 = &local_88;
  do {
    puVar31 = (undefined8 *)((long)puVar32 + 1);
    *(undefined1 *)puVar32 = 0;
    puVar32 = puVar31;
  } while (puVar31 != &local_48);
  puVar32 = &local_a8;
  do {
    puVar31 = (undefined8 *)((long)puVar32 + 1);
    *(undefined1 *)puVar32 = 0;
    puVar32 = puVar31;
  } while (puVar31 != &local_88);
  FUN_00101df0(&local_128,param_3,0x18);
  iVar36 = 0;
  FUN_00101df0(&local_128,param_3 + 0x28,param_4);
  FUN_00101df0(&local_128,"spi-tpm-route",0xd);
  do {
    uVar28 = (iVar36 * -0x61c88647 ^ uVar3 ^ uVar4 ^ 0x726f7574) + 0x9e3779b9;
    uVar28 = (uVar28 >> 0x10 ^ uVar28) * 0x21f0aaad;
    uVar28 = (uVar28 >> 0xf ^ uVar28) * 0x735a2d97;
    uVar29 = FUN_001017e0(uVar28 >> 0xf ^ uVar28,uVar4,iVar36 + -0x80000000,iVar2,0,0);
    iVar30 = FUN_00103700(param_2 + 0x10,uVar29,iVar2,0);
    *(uint *)(param_1 + 0x2440) = *(uint *)(param_1 + 0x2440) ^ iVar2 + iVar30;
    iVar1 = iVar36 + -0x80000000;
    iVar36 = iVar36 + 1;
    uVar29 = FUN_001017e0(iVar30,uVar4,iVar1,iVar2);
    local_88 = CONCAT44(local_88._4_4_,uVar29);
    FUN_00101df0(&local_128,&local_88,4);
    auVar66 = local_108;
  } while (iVar36 != 0x20);
  bVar37 = CARRY4(local_108._0_4_,local_c8._8_4_);
  iVar2 = local_108._0_4_ + local_c8._8_4_;
  local_108._0_4_ = iVar2;
  if (bVar37) {
    local_108._4_4_ = auVar66._4_4_;
    local_108._8_8_ = auVar66._8_8_;
    local_108._4_4_ = local_108._4_4_ + 1;
  }
  uVar33 = 0x78;
  if (0x77 < local_c8._8_8_ + 0x28) {
    uVar33 = local_c8._8_8_ + 0x28;
  }
  __memset_chk(local_108 + local_c8._8_8_ + 8,0,0x40 - local_c8._8_8_,
               (uVar33 - local_c8._8_8_) + -0x28);
  FUN_00101200(&local_128,1);
  auVar84._8_8_ = 0;
  auVar84._0_8_ = DAT_001041c0;
  auVar66 = ZEXT716(CONCAT34((int3)(CONCAT16((char)((ulong)uStack_120 >> 0x38),
                                             (uint6)(byte)((ulong)uStack_120 >> 0x18) << 0x20) >>
                                   0x20),
                             (uint)CONCAT12((char)(local_128 >> 0x38),
                                            (ushort)(byte)(local_128 >> 0x18)))) & auVar84;
  auVar109 = ZEXT716(CONCAT34((int3)(CONCAT16((char)((ulong)uStack_110 >> 0x38),
                                              (uint6)(byte)((ulong)uStack_110 >> 0x18) << 0x20) >>
                                    0x20),
                              (uint)CONCAT12((char)(local_118 >> 0x38),
                                             (ushort)(byte)(local_118 >> 0x18)))) & auVar84;
  uVar61 = auVar66._0_2_;
  uVar107 = auVar66._2_2_;
  uVar112 = auVar66._4_2_;
  uVar113 = auVar66._6_2_;
  uVar108 = auVar109._0_2_;
  cVar6 = (uVar108 != 0) * (uVar108 < 0x100) * auVar109[0] - (0xff < uVar108);
  uVar108 = auVar109._2_2_;
  cVar7 = (uVar108 != 0) * (uVar108 < 0x100) * auVar109[2] - (0xff < uVar108);
  uVar108 = auVar109._4_2_;
  cVar8 = (uVar108 != 0) * (uVar108 < 0x100) * auVar109[4] - (0xff < uVar108);
  uVar108 = auVar109._6_2_;
  cVar9 = (uVar108 != 0) * (uVar108 < 0x100) * auVar109[6] - (0xff < uVar108);
  uVar111 = (ushort)((ulong)uStack_120 >> 0x30);
  uVar126 = (ushort)(local_128 >> 0x30);
  uVar108 = (ushort)((ulong)uStack_120 >> 0x10);
  uVar114 = (ushort)(local_128 >> 0x10);
  uVar33 = CONCAT44(CONCAT22(uVar111,uVar108),CONCAT22(uVar126,uVar114)) & DAT_001041c0;
  uVar127 = (ushort)((ulong)uStack_110 >> 0x30);
  uVar130 = (ushort)(local_118 >> 0x30);
  uVar115 = (ushort)((ulong)uStack_110 >> 0x10);
  uVar129 = (ushort)(local_118 >> 0x10);
  uVar27 = CONCAT44(CONCAT22(uVar127,uVar115),CONCAT22(uVar130,uVar129)) & DAT_001041c0;
  sVar5 = (short)uVar33;
  cVar10 = (0 < sVar5) * (sVar5 < 0x100) * (char)uVar33 - (0xff < sVar5);
  sVar5 = (short)(uVar33 >> 0x10);
  cVar11 = (0 < sVar5) * (sVar5 < 0x100) * (char)(uVar33 >> 0x10) - (0xff < sVar5);
  uVar63 = CONCAT11(cVar11,cVar10);
  sVar5 = (short)(uVar33 >> 0x20);
  cVar12 = (0 < sVar5) * (sVar5 < 0x100) * (char)(uVar33 >> 0x20) - (0xff < sVar5);
  uVar64 = CONCAT12(cVar12,uVar63);
  sVar5 = (short)(uVar33 >> 0x30);
  cVar13 = (0 < sVar5) * (sVar5 < 0x100) * (char)(uVar33 >> 0x30) - (0xff < sVar5);
  uVar29 = CONCAT13(cVar13,uVar64);
  sVar5 = (short)uVar27;
  cVar14 = (0 < sVar5) * (sVar5 < 0x100) * (char)uVar27 - (0xff < sVar5);
  sVar5 = (short)(uVar27 >> 0x10);
  cVar15 = (0 < sVar5) * (sVar5 < 0x100) * (char)(uVar27 >> 0x10) - (0xff < sVar5);
  sVar5 = (short)(uVar27 >> 0x20);
  cVar16 = (0 < sVar5) * (sVar5 < 0x100) * (char)(uVar27 >> 0x20) - (0xff < sVar5);
  sVar5 = (short)(uVar27 >> 0x30);
  bVar17 = (0 < sVar5) * (sVar5 < 0x100) * (char)(uVar27 >> 0x30) - (0xff < sVar5);
  auVar65._0_8_ = CONCAT44((uint)bVar17 << 0x18,uVar29);
  auVar65._8_4_ = uVar29;
  auVar67._12_4_ = uVar29;
  auVar67._0_12_ = auVar65;
  auVar74._0_14_ = auVar67._0_14_;
  auVar74[0xe] = bVar17;
  auVar74[0xf] = cVar9;
  auVar73._14_2_ = auVar74._14_2_;
  auVar73._0_13_ = auVar67._0_13_;
  auVar73[0xd] = cVar8;
  auVar72._13_3_ = auVar73._13_3_;
  auVar72[0xc] = cVar16;
  auVar72._0_12_ = auVar65;
  auVar71._12_4_ = auVar72._12_4_;
  auVar71._0_11_ = auVar65._0_11_;
  auVar71[0xb] = cVar7;
  auVar70._11_5_ = auVar71._11_5_;
  auVar70._0_10_ = auVar65._0_10_;
  auVar70[10] = cVar15;
  auVar69._10_6_ = auVar70._10_6_;
  auVar69._0_9_ = auVar65._0_9_;
  auVar69[9] = cVar6;
  auVar68._9_7_ = auVar69._9_7_;
  auVar68[8] = cVar14;
  auVar68._0_8_ = auVar65._0_8_;
  auVar125[0xe] = bVar17;
  auVar125._0_14_ = auVar74._0_14_;
  auVar125[0xf] = cVar9;
  auVar124._14_2_ = auVar125._14_2_;
  auVar124[0xd] = cVar8;
  auVar124._0_13_ = auVar73._0_13_;
  auVar123._13_3_ = auVar124._13_3_;
  auVar123[0xc] = cVar16;
  auVar123._0_12_ = auVar65;
  auVar122._12_4_ = auVar123._12_4_;
  auVar122[0xb] = cVar7;
  auVar122._0_11_ = auVar71._0_11_;
  auVar121._11_5_ = auVar122._11_5_;
  auVar121[10] = cVar15;
  auVar121._0_10_ = auVar70._0_10_;
  auVar120._10_6_ = auVar121._10_6_;
  auVar120[9] = cVar6;
  auVar120._0_9_ = auVar69._0_9_;
  auVar119._9_7_ = auVar120._9_7_;
  auVar119[8] = cVar14;
  auVar119._0_8_ = auVar65._0_8_;
  Var21 = CONCAT91(CONCAT81(auVar119._8_8_,
                            (uVar113 != 0) * (uVar113 < 0x100) * auVar66[6] - (0xff < uVar113)),
                   cVar13);
  auVar118._6_10_ = Var21;
  auVar118[5] = (uVar112 != 0) * (uVar112 < 0x100) * auVar66[4] - (0xff < uVar112);
  auVar118[4] = cVar12;
  auVar118._0_4_ = uVar29;
  auVar117._4_12_ = auVar118._4_12_;
  auVar117[3] = (uVar107 != 0) * (uVar107 < 0x100) * auVar66[2] - (0xff < uVar107);
  auVar117._0_3_ = uVar64;
  auVar116._3_13_ = auVar117._3_13_;
  auVar116[2] = cVar11;
  auVar116._0_2_ = uVar63;
  auVar76[3] = (uVar61 != 0) * (uVar61 < 0x100) * auVar66[0] - (0xff < uVar61);
  auVar76[2] = cVar10;
  auVar42._8_4_ = 0;
  auVar42._0_8_ = local_128;
  auVar42._12_2_ = uVar126;
  auVar42._14_2_ = uVar111;
  auVar41._12_4_ = auVar42._12_4_;
  auVar41._8_2_ = 0;
  auVar41._0_8_ = local_128;
  uVar113 = (ushort)((ulong)uStack_120 >> 0x20);
  auVar41._10_2_ = uVar113;
  uVar61 = (ushort)(local_128 >> 0x20);
  auVar40._10_6_ = auVar41._10_6_;
  auVar40._8_2_ = uVar61;
  auVar40._0_8_ = local_128;
  auVar109._2_8_ = auVar40._8_8_;
  auVar109._0_2_ = uVar108;
  auVar109._10_6_ = 0;
  auVar43._0_2_ = (ushort)local_128;
  auVar66._12_4_ = 0;
  auVar66._0_12_ = SUB1612(auVar109 << 0x30,4);
  auVar66 = auVar66 << 0x20;
  auVar46._0_12_ = auVar66._0_12_;
  auVar46._12_2_ = uVar108;
  auVar46._14_2_ = uVar111;
  auVar45._12_4_ = auVar46._12_4_;
  auVar45._0_10_ = auVar66._0_10_;
  auVar45._10_2_ = uVar126;
  auVar44._10_6_ = auVar45._10_6_;
  auVar44._0_8_ = auVar66._0_8_;
  auVar44._8_2_ = uVar114;
  auVar43._8_8_ = auVar44._8_8_;
  auVar43._6_2_ = uVar113;
  auVar43._4_2_ = (ushort)uStack_120;
  auVar43._2_2_ = uVar61;
  auVar102._8_4_ = 0;
  auVar102._0_8_ = local_118;
  auVar102._12_2_ = uVar130;
  auVar102._14_2_ = uVar127;
  auVar101._12_4_ = auVar102._12_4_;
  auVar101._8_2_ = 0;
  auVar101._0_8_ = local_118;
  uVar112 = (ushort)((ulong)uStack_110 >> 0x20);
  auVar101._10_2_ = uVar112;
  uVar107 = (ushort)(local_118 >> 0x20);
  auVar100._10_6_ = auVar101._10_6_;
  auVar100._8_2_ = uVar107;
  auVar100._0_8_ = local_118;
  auVar22._2_8_ = auVar100._8_8_;
  auVar22._0_2_ = uVar115;
  auVar22._10_6_ = 0;
  auVar103._0_2_ = (ushort)local_118;
  auVar99._12_4_ = 0;
  auVar99._0_12_ = SUB1612(auVar22 << 0x30,4);
  auVar99 = auVar99 << 0x20;
  auVar106._0_12_ = auVar99._0_12_;
  auVar106._12_2_ = uVar115;
  auVar106._14_2_ = uVar127;
  auVar105._12_4_ = auVar106._12_4_;
  auVar105._0_10_ = auVar99._0_10_;
  auVar105._10_2_ = uVar130;
  auVar104._10_6_ = auVar105._10_6_;
  auVar104._0_8_ = auVar99._0_8_;
  auVar104._8_2_ = uVar129;
  auVar103._8_8_ = auVar104._8_8_;
  auVar103._6_2_ = uVar112;
  auVar103._4_2_ = (ushort)uStack_110;
  auVar103._2_2_ = uVar107;
  auVar66 = auVar43 & auVar84;
  auVar75._0_2_ = auVar43._0_2_ >> 8;
  auVar75._2_2_ = uVar61 >> 8;
  auVar75._4_2_ = (ushort)uStack_120 >> 8;
  auVar75._6_2_ = uVar113 >> 8;
  auVar75._8_2_ = uVar114 >> 8;
  auVar75._10_2_ = uVar126 >> 8;
  auVar75._12_2_ = uVar108 >> 8;
  auVar75._14_2_ = uVar111 >> 8;
  auVar110._0_2_ = auVar103._0_2_ >> 8;
  auVar110._2_2_ = uVar107 >> 8;
  auVar110._4_2_ = (ushort)uStack_110 >> 8;
  auVar110._6_2_ = uVar112 >> 8;
  auVar110._8_2_ = uVar129 >> 8;
  auVar110._10_2_ = uVar130 >> 8;
  auVar110._12_2_ = uVar115 >> 8;
  auVar110._14_2_ = uVar127 >> 8;
  auVar75 = auVar75 & auVar84;
  auVar110 = auVar110 & auVar84;
  auVar84 = auVar84 & auVar103;
  sVar5 = auVar66._0_2_;
  cVar12 = (0 < sVar5) * (sVar5 < 0x100) * auVar66[0] - (0xff < sVar5);
  sVar5 = auVar66._2_2_;
  cVar7 = (0 < sVar5) * (sVar5 < 0x100) * auVar66[2] - (0xff < sVar5);
  auVar49._0_2_ = CONCAT11(cVar7,cVar12);
  sVar5 = auVar66._4_2_;
  cVar11 = (0 < sVar5) * (sVar5 < 0x100) * auVar66[4] - (0xff < sVar5);
  auVar50._0_3_ = CONCAT12(cVar11,auVar49._0_2_);
  sVar5 = auVar66._6_2_;
  cVar10 = (0 < sVar5) * (sVar5 < 0x100) * auVar66[6] - (0xff < sVar5);
  uVar29 = CONCAT13(cVar10,auVar50._0_3_);
  sVar5 = auVar84._0_2_;
  cVar6 = (0 < sVar5) * (sVar5 < 0x100) * auVar84[0] - (0xff < sVar5);
  sVar5 = auVar84._2_2_;
  cVar9 = (0 < sVar5) * (sVar5 < 0x100) * auVar84[2] - (0xff < sVar5);
  sVar5 = auVar84._4_2_;
  cVar8 = (0 < sVar5) * (sVar5 < 0x100) * auVar84[4] - (0xff < sVar5);
  sVar5 = auVar84._6_2_;
  bVar17 = (0 < sVar5) * (sVar5 < 0x100) * auVar84[6] - (0xff < sVar5);
  uVar61 = auVar75._0_2_;
  cVar13 = (uVar61 != 0) * (uVar61 < 0x100) * auVar75[0] - (0xff < uVar61);
  uVar61 = auVar75._2_2_;
  cVar14 = (uVar61 != 0) * (uVar61 < 0x100) * auVar75[2] - (0xff < uVar61);
  uVar61 = auVar75._4_2_;
  uVar107 = auVar75._6_2_;
  cVar15 = (uVar107 != 0) * (uVar107 < 0x100) * auVar75[6] - (0xff < uVar107);
  uVar107 = auVar110._0_2_;
  cVar16 = (uVar107 != 0) * (uVar107 < 0x100) * auVar110[0] - (0xff < uVar107);
  uVar107 = auVar110._2_2_;
  cVar18 = (uVar107 != 0) * (uVar107 < 0x100) * auVar110[2] - (0xff < uVar107);
  uVar107 = auVar110._4_2_;
  cVar19 = (uVar107 != 0) * (uVar107 < 0x100) * auVar110[4] - (0xff < uVar107);
  uVar107 = auVar110._6_2_;
  cVar20 = (uVar107 != 0) * (uVar107 < 0x100) * auVar110[6] - (0xff < uVar107);
  auVar38._0_8_ = CONCAT44((int)(((uint5)bVar17 << 0x20) >> 8),uVar29);
  auVar38._8_4_ = uVar29;
  auVar47._12_4_ = uVar29;
  auVar47._0_12_ = auVar38;
  auVar57._0_14_ = auVar47._0_14_;
  auVar57[0xe] = bVar17;
  auVar57[0xf] = cVar20;
  auVar56._14_2_ = auVar57._14_2_;
  auVar56._0_13_ = auVar47._0_13_;
  auVar56[0xd] = cVar19;
  auVar55._13_3_ = auVar56._13_3_;
  auVar55[0xc] = cVar8;
  auVar55._0_12_ = auVar38;
  auVar54._12_4_ = auVar55._12_4_;
  auVar54._0_11_ = auVar38._0_11_;
  auVar54[0xb] = cVar18;
  auVar53._11_5_ = auVar54._11_5_;
  auVar53._0_10_ = auVar38._0_10_;
  auVar53[10] = cVar9;
  auVar52._10_6_ = auVar53._10_6_;
  auVar52._0_9_ = auVar38._0_9_;
  auVar52[9] = cVar16;
  auVar51._9_7_ = auVar52._9_7_;
  auVar51[8] = cVar6;
  auVar51._0_8_ = auVar38._0_8_;
  uVar62 = auVar51._8_8_;
  auVar25._1_8_ = uVar62;
  auVar25[0] = cVar15;
  auVar25._9_7_ = 0;
  auVar24._10_6_ = 0;
  auVar24._0_10_ = SUB1610(auVar25 << 0x38,6);
  auVar23._11_5_ = 0;
  auVar23._0_11_ = SUB1611(auVar24 << 0x30,5);
  auVar50._4_12_ = SUB1612(auVar23 << 0x28,4);
  auVar50[3] = cVar14;
  auVar49._3_13_ = auVar50._3_13_;
  auVar49[2] = cVar7;
  auVar48._2_14_ = auVar49._2_14_;
  auVar48[1] = cVar13;
  auVar48[0] = cVar12;
  auVar95[0xe] = bVar17;
  auVar95._0_14_ = auVar57._0_14_;
  auVar95[0xf] = cVar20;
  auVar94._14_2_ = auVar95._14_2_;
  auVar94[0xd] = cVar19;
  auVar94._0_13_ = auVar56._0_13_;
  auVar93._13_3_ = auVar94._13_3_;
  auVar93[0xc] = cVar8;
  auVar93._0_12_ = auVar38;
  auVar92._12_4_ = auVar93._12_4_;
  auVar92[0xb] = cVar18;
  auVar92._0_11_ = auVar54._0_11_;
  auVar91._11_5_ = auVar92._11_5_;
  auVar91[10] = cVar9;
  auVar91._0_10_ = auVar53._0_10_;
  auVar90._10_6_ = auVar91._10_6_;
  auVar90[9] = cVar16;
  auVar90._0_9_ = auVar52._0_9_;
  auVar89._9_7_ = auVar90._9_7_;
  auVar89[8] = cVar6;
  auVar89._0_8_ = auVar38._0_8_;
  Var26 = CONCAT91(CONCAT81(auVar89._8_8_,cVar15),cVar10);
  auVar88._6_10_ = Var26;
  auVar88[5] = (uVar61 != 0) * (uVar61 < 0x100) * auVar75[4] - (0xff < uVar61);
  auVar88[4] = cVar11;
  auVar88._0_4_ = uVar29;
  auVar87._4_12_ = auVar88._4_12_;
  auVar87[3] = cVar14;
  auVar87._0_3_ = auVar50._0_3_;
  auVar86._3_13_ = auVar87._3_13_;
  auVar86[2] = cVar7;
  auVar86._0_2_ = auVar49._0_2_;
  auVar85._2_14_ = auVar86._2_14_;
  auVar85._0_2_ = CONCAT11(cVar13,cVar12);
  auVar39._8_4_ = auVar48._0_4_;
  auVar39._0_8_ = uVar62;
  uVar128 = (undefined2)Var21;
  uVar63 = (undefined2)Var26;
  auVar98._0_12_ = auVar85._0_12_;
  auVar98._12_2_ = uVar63;
  auVar98._14_2_ = uVar128;
  auVar97._12_4_ = auVar98._12_4_;
  auVar97._0_10_ = auVar85._0_10_;
  auVar97._10_2_ = auVar118._4_2_;
  auVar96._10_6_ = auVar97._10_6_;
  auVar96._0_8_ = auVar85._0_8_;
  auVar96._8_2_ = auVar88._4_2_;
  auVar79._12_2_ = uVar63;
  auVar79._0_12_ = auVar98._0_12_;
  auVar79._14_2_ = uVar128;
  auVar78._12_4_ = auVar79._12_4_;
  auVar78._10_2_ = auVar118._4_2_;
  auVar78._0_10_ = auVar97._0_10_;
  auVar77._10_6_ = auVar78._10_6_;
  auVar77._8_2_ = auVar88._4_2_;
  auVar77._0_8_ = auVar96._0_8_;
  auVar76._8_8_ = auVar77._8_8_;
  auVar76._6_2_ = auVar116._2_2_;
  auVar76._4_2_ = auVar86._2_2_;
  auVar76._0_2_ = auVar85._0_2_;
  uStack_80 = CONCAT44(auVar97._12_4_,auVar96._8_4_);
  local_88 = auVar76._0_8_;
  auVar60._12_2_ = auVar56._14_2_;
  auVar60._0_12_ = auVar39;
  auVar60._14_2_ = auVar73._14_2_;
  auVar59._12_4_ = auVar60._12_4_;
  auVar59._0_10_ = auVar39._0_10_;
  auVar59._10_2_ = auVar72._12_2_;
  auVar58._10_6_ = auVar59._10_6_;
  auVar58._8_2_ = auVar55._12_2_;
  auVar58._0_8_ = uVar62;
  auVar83._12_2_ = auVar56._14_2_;
  auVar83._0_12_ = auVar39;
  auVar83._14_2_ = auVar73._14_2_;
  auVar82._12_4_ = auVar83._12_4_;
  auVar82._10_2_ = auVar72._12_2_;
  auVar82._0_10_ = auVar59._0_10_;
  auVar81._10_6_ = auVar82._10_6_;
  auVar81._8_2_ = auVar55._12_2_;
  auVar81._0_8_ = uVar62;
  auVar80._8_8_ = auVar81._8_8_;
  auVar80._6_2_ = auVar70._10_2_;
  auVar80._4_2_ = auVar53._10_2_;
  auVar80._2_2_ = auVar68._8_2_;
  auVar80._0_2_ = auVar51._8_2_;
  uStack_70 = CONCAT44(auVar59._12_4_,auVar58._8_4_);
  local_78 = auVar80._0_8_;
  memcpy(param_5,&local_88,local_b8);
  puVar32 = &local_88;
  do {
    puVar31 = (undefined8 *)((long)puVar32 + 1);
    *(undefined1 *)puVar32 = 0;
    puVar32 = puVar31;
  } while (puVar31 != (undefined8 *)local_68);
  puVar34 = &local_128;
  do {
    puVar35 = (ulong *)((long)puVar34 + 1);
    *(undefined1 *)puVar34 = 0;
    puVar34 = puVar35;
  } while (puVar35 != &local_b0);
  if (local_40 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00102350 @ 00102350 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_00102350(void *param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  char cVar3;
  
  if (param_1 == (void *)0x0) {
    return;
  }
  memset(param_1,0,0x24b0);
  cVar3 = FUN_00101ca0(param_1);
  uVar2 = s__failed_to_reseed_firmware_key_t_0010415f._9_8_;
  uVar1 = s__failed_to_reseed_firmware_key_t_0010415f._1_8_;
  if (cVar3 != '\0') {
    FUN_00101ad0(param_1);
    return;
  }
  *(undefined4 *)((long)param_1 + 0x2464) = 0x656c62;
  *(undefined8 *)((long)param_1 + 0x2444) = uVar1;
  *(undefined8 *)((long)param_1 + 0x244c) = uVar2;
  uVar1 = s__failed_to_reseed_firmware_key_t_0010415f._25_8_;
  *(undefined8 *)((long)param_1 + 0x2454) = s__failed_to_reseed_firmware_key_t_0010415f._17_8_;
  *(undefined8 *)((long)param_1 + 0x245c) = uVar1;
  FUN_00101ad0(param_1);
  return;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_001023c0 @ 001023c0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined8 FUN_001023c0(void *param_1,int *param_2,long param_3)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  undefined8 uVar5;
  undefined1 *__dest;
  undefined1 *puVar6;
  void *pvVar7;
  byte *pbVar8;
  undefined1 *puVar9;
  uint uVar10;
  long lVar11;
  char *pcVar12;
  char *pcVar13;
  byte bVar14;
  
  uVar5 = s__failed_to_reseed_firmware_key_t_0010415f._41_8_;
  bVar14 = 0;
  if (param_1 == (void *)0x0) {
    return 0xffffffff;
  }
  if (param_2 == (int *)0x0) {
    if (param_1 == (void *)0x0) {
      return 0xffffffff;
    }
LAB_00102583:
    *(undefined8 *)((long)param_1 + 0x2444) = s__failed_to_reseed_firmware_key_t_0010415f._33_8_;
    *(undefined8 *)((long)param_1 + 0x244c) = uVar5;
    uVar5 = s__failed_to_reseed_firmware_key_t_0010415f._57_8_;
    *(undefined8 *)((long)param_1 + 0x244e) = s__failed_to_reseed_firmware_key_t_0010415f._49_8_;
    *(undefined8 *)((long)param_1 + 0x2456) = uVar5;
    return 0xffffffff;
  }
  if (((param_3 != 0x24b8) || (*param_2 != 0x43524657)) || (param_2[1] != 5)) goto LAB_00102583;
  __dest = malloc(0x24b0);
  if (__dest == (undefined1 *)0x0) {
    pcVar12 = "failed to allocate firmware snapshot";
    pcVar13 = (char *)((long)param_1 + 0x2444);
    for (lVar11 = 0x25; lVar11 != 0; lVar11 = lVar11 + -1) {
      *pcVar13 = *pcVar12;
      pcVar12 = pcVar12 + (ulong)bVar14 * -2 + 1;
      pcVar13 = pcVar13 + (ulong)bVar14 * -2 + 1;
    }
    return 0xffffffff;
  }
  memcpy(__dest,param_2 + 2,0x24b0);
  uVar1 = *(uint *)(__dest + 0x2424);
  if (((((0x1ff4 < uVar1 - 0x10) || (uVar1 < *(uint *)(__dest + 0x2420))) ||
       ((uVar2 = *(uint *)(__dest + 0x2428), 0x1000 < uVar2 - 0x10 ||
        ((uVar1 < uVar2 || (uVar3 = *(uint *)(__dest + 0x242c), uVar3 < uVar2)))))) ||
      (uVar1 < uVar3)) ||
     (((uVar4 = *(uint *)(__dest + 0x2430), 0x1008 < uVar4 || (uVar1 - uVar3 < uVar4)) ||
      (uVar10 = *(uint *)(__dest + 0x2434), 0x2004 < uVar10)))) goto LAB_00102460;
  if (uVar10 == 0) {
    if (uVar4 != 0) {
      uVar10 = uVar3 + uVar4;
joined_r0x001025b3:
      if (uVar1 != uVar10) goto LAB_00102460;
    }
  }
  else {
    if (uVar10 < uVar2 + 8) goto LAB_00102460;
    if (uVar4 != 0) goto joined_r0x001025b3;
  }
  pvVar7 = memchr(__dest + 0x2444,0,0x60);
  if (pvVar7 != (void *)0x0) {
    pbVar8 = __dest + 0x2090;
    while (*pbVar8 < 2) {
      pbVar8 = pbVar8 + 0x80;
      if (__dest + 0x2490 == pbVar8) {
        memcpy(param_1,__dest,0x24b0);
        puVar9 = __dest;
        do {
          puVar6 = puVar9 + 1;
          *puVar9 = 0;
          puVar9 = puVar6;
        } while (__dest + 0x24b0 != puVar6);
        free(__dest);
        return 0;
      }
    }
  }
LAB_00102460:
  puVar9 = __dest;
  do {
    puVar6 = puVar9 + 1;
    *puVar9 = 0;
    puVar9 = puVar6;
  } while (puVar6 != __dest + 0x24b0);
  free(__dest);
  uVar5 = s_invalid_snapshothot_frame_state_001041a0._8_8_;
  *(undefined8 *)((long)param_1 + 0x2444) = s_invalid_snapshothot_frame_state_001041a0._0_8_;
  *(undefined8 *)((long)param_1 + 0x244c) = uVar5;
  uVar5 = s_invalid_snapshothot_frame_state_001041a0._24_8_;
  *(undefined8 *)((long)param_1 + 0x2451) = s_invalid_snapshothot_frame_state_001041a0._16_8_;
  *(undefined8 *)((long)param_1 + 0x2459) = uVar5;
  return 0xffffffff;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_001025e0 @ 001025e0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_001025e0(char *param_1)

{
  ushort uVar1;
  undefined2 uVar2;
  int iVar3;
  char cVar4;
  int iVar5;
  undefined4 uVar6;
  uint uVar7;
  uint uVar8;
  int iVar9;
  int iVar10;
  undefined4 uVar11;
  uint uVar12;
  int *piVar13;
  undefined4 *puVar14;
  undefined4 *puVar15;
  ulong uVar16;
  char *pcVar17;
  ulong uVar18;
  char *pcVar19;
  long lVar20;
  uint uVar21;
  uint uVar22;
  uint uVar23;
  long in_FS_OFFSET;
  undefined1 auVar24 [16];
  uint local_a0;
  char *local_90;
  undefined4 local_5c;
  undefined4 local_58;
  undefined1 auStack_54 [12];
  undefined4 local_48 [2];
  long local_40;
  
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  if (*param_1 == -0x5b) {
    cVar4 = param_1[1];
    uVar1 = *(ushort *)(param_1 + 2);
    uVar8 = (uint)uVar1;
    if (cVar4 == '\x02') {
      uVar18 = 0;
      piVar13 = (int *)(param_1 + 0x2020);
      do {
        if (((char)piVar13[0x1c] != '\0') && (*(int *)(param_1 + 4) == *piVar13)) {
          iVar5 = *(int *)(param_1 + 8);
          uVar2 = *(undefined2 *)(param_1 + 8);
          if ((iVar5 - 1U < 1000000) && (uVar1 < 0xfd9)) {
            cVar4 = FUN_00101b90(&local_5c,4);
            if (cVar4 != '\0') {
              uVar23 = uVar8 + 3;
              local_a0 = uVar23 & 0xfffffffc;
              FUN_00101b20(param_1,0,((ushort)uVar23 & 0xfffc) + 0x28);
              puVar14 = &local_5c;
              do {
                puVar15 = (undefined4 *)((long)puVar14 + 1);
                *(undefined1 *)puVar14 = 0;
                puVar14 = puVar15;
              } while (puVar15 != &local_58);
              *(ushort *)(param_1 + 0x1028) = uVar1;
              param_1[0x1018] = 'S';
              param_1[0x1019] = 'T';
              param_1[0x101a] = 'P';
              param_1[0x101b] = '1';
              param_1[0x101c] = '\x02';
              param_1[0x101d] = '\0';
              param_1[0x101e] = '(';
              param_1[0x101f] = '\0';
              *(undefined4 *)(param_1 + 0x1020) = local_5c;
              param_1[0x1026] = (char)((uint)iVar5 >> 0x10);
              param_1[0x102a] = '\0';
              param_1[0x102b] = '\0';
              *(undefined2 *)(param_1 + 0x1024) = uVar2;
              param_1[0x1027] = '\0';
              uVar6 = FUN_00103850(param_1 + uVar18 * 0x80 + 0x2030,local_5c,
                                   *(undefined4 *)(param_1 + 0x243c));
              *(undefined4 *)(param_1 + 0x102c) = uVar6;
              *(undefined1 (*) [16])(param_1 + 0x1030) = (undefined1  [16])0x0;
              if (local_a0 != 0) {
                uVar21 = 0;
                pcVar19 = param_1 + 0x10;
                uVar12 = uVar8;
                do {
                  local_58 = 0;
                  if (uVar21 < uVar8) {
                    if (uVar12 < 5) {
                      uVar22 = uVar12;
                      if (uVar12 == 0) goto LAB_001029d0;
                    }
                    else {
                      uVar22 = 4;
                    }
                    if (uVar22 != 0) {
                      uVar7 = 0;
                      do {
                        uVar16 = (ulong)uVar7;
                        uVar7 = uVar7 + 1;
                        *(char *)((long)&local_58 + uVar16) = pcVar19[uVar16];
                      } while (uVar7 < uVar22);
                    }
                  }
LAB_001029d0:
                  uVar22 = uVar21 >> 2;
                  uVar21 = uVar21 + 4;
                  uVar12 = uVar12 - 4;
                  uVar6 = FUN_001017e0(0,local_5c,uVar22,iVar5,0,0);
                  iVar9 = FUN_00103700(param_1 + uVar18 * 0x80 + 0x2030,uVar6,iVar5,0);
                  *(uint *)(param_1 + 0x2440) = *(uint *)(param_1 + 0x2440) ^ iVar5 + iVar9;
                  uVar6 = FUN_001017e0(iVar9,local_5c,uVar22,iVar5);
                  pcVar19[0x1030] = (char)uVar6;
                  pcVar19[0x1031] = (char)((uint)uVar6 >> 8);
                  pcVar19[0x1032] = (char)((uint)uVar6 >> 0x10);
                  pcVar19[0x1033] = (char)((uint)uVar6 >> 0x18);
                  pcVar19 = pcVar19 + 4;
                } while (uVar21 < local_a0);
              }
              FUN_00101ea0(param_1,param_1 + uVar18 * 0x80 + 0x2020,param_1 + 0x1018,
                           uVar23 & 0xfffffffc,param_1 + 0x1030);
              goto LAB_001026cb;
            }
            memset(param_1 + 0x1010,0xff,0x1008);
            iVar5 = *(int *)(param_1 + 0x2434);
            param_1[0x1010] = -0x5b;
            param_1[0x1011] = -0x19;
            param_1[0x1012] = '\0';
            param_1[0x1013] = '\0';
            param_1[0x1014] = '\0';
            param_1[0x1015] = '\0';
            param_1[0x1016] = '\0';
            param_1[0x1017] = '\0';
            param_1[0x2430] = '\b';
            param_1[0x2431] = '\0';
            param_1[0x2432] = '\0';
            param_1[0x2433] = '\0';
          }
          else {
            memset(param_1 + 0x1010,0xff,0x1008);
            iVar5 = *(int *)(param_1 + 0x2434);
            param_1[0x1010] = -0x5b;
            param_1[0x1011] = -0x1d;
            param_1[0x1012] = '\0';
            param_1[0x1013] = '\0';
            param_1[0x1014] = '\0';
            param_1[0x1015] = '\0';
            param_1[0x1016] = '\0';
            param_1[0x1017] = '\0';
            param_1[0x2430] = '\b';
            param_1[0x2431] = '\0';
            param_1[0x2432] = '\0';
            param_1[0x2433] = '\0';
          }
          if (iVar5 == 0) {
            iVar5 = *(int *)(param_1 + 0x242c) + 8;
          }
          goto LAB_00102680;
        }
        uVar23 = (int)uVar18 + 1;
        uVar18 = (ulong)uVar23;
        piVar13 = piVar13 + 0x20;
      } while (uVar23 != 8);
      memset(param_1 + 0x1010,0xff,0x1008);
      iVar5 = *(int *)(param_1 + 0x2434);
      param_1[0x1010] = -0x5b;
      param_1[0x1011] = -0x1c;
      param_1[0x1012] = '\0';
      param_1[0x1013] = '\0';
      param_1[0x1014] = '\0';
      param_1[0x1015] = '\0';
      param_1[0x1016] = '\0';
      param_1[0x1017] = '\0';
      param_1[0x2430] = '\b';
      param_1[0x2431] = '\0';
      param_1[0x2432] = '\0';
      param_1[0x2433] = '\0';
joined_r0x00102ba0:
      if (iVar5 == 0) {
        iVar5 = *(int *)(param_1 + 0x242c) + 8;
      }
LAB_00102680:
      *(int *)(param_1 + 0x2424) = iVar5;
      goto LAB_001026cb;
    }
    if (cVar4 == '\x03') {
      if ((((0x27 < uVar1) && (*(int *)(param_1 + 0x10) == 0x31505453)) &&
          (*(short *)(param_1 + 0x14) == 2)) && (*(short *)(param_1 + 0x16) == 0x28)) {
        iVar5 = *(int *)(param_1 + 0x1c);
        uVar23 = *(uint *)(param_1 + 0x20);
        if ((iVar5 - 1U < 1000000) && (uVar23 < 0xfd9)) {
          uVar12 = uVar23 + 3;
          local_a0 = uVar12 & 0xfffffffc;
          if (uVar8 == (uVar12 & 0xfffffffc) + 0x28) {
            uVar6 = *(undefined4 *)(param_1 + 0x18);
            local_90 = (char *)0x0;
            iVar9 = 0;
            pcVar19 = param_1 + 0x2020;
            do {
              FUN_00101ea0(param_1,pcVar19,param_1 + 0x10,uVar12 & 0xfffffffc,&local_58);
              auVar24._4_12_ = auStack_54;
              auVar24._0_4_ = local_58;
              auVar24 = *(undefined1 (*) [16])(param_1 + 0x28) ^ auVar24 |
                        (*(undefined1 (*) [16])(param_1 + 0x28) ^ auVar24) >> 0x40;
              auVar24 = auVar24 | auVar24 >> 0x20;
              auVar24 = auVar24 | auVar24 >> 0x10;
              puVar14 = &local_58;
              if ((auVar24[0] == '\0' && auVar24[1] == '\0') && (pcVar19[0x70] != '\0')) {
                iVar3 = *(int *)(param_1 + 0x24);
                iVar10 = FUN_00103850(pcVar19 + 0x10,uVar6,*(undefined4 *)(param_1 + 0x243c));
                if (iVar3 == iVar10) {
                  local_90 = pcVar19;
                  iVar9 = iVar9 + 1;
                }
              }
              do {
                puVar15 = (undefined4 *)((long)puVar14 + 1);
                *(undefined1 *)puVar14 = 0;
                puVar14 = puVar15;
              } while (puVar15 != local_48);
              pcVar19 = pcVar19 + 0x80;
            } while (pcVar19 != param_1 + 0x2420);
            if (iVar9 == 1) {
              FUN_00101b20(param_1,0,uVar23 & 0xffff);
              if (local_a0 != 0) {
                pcVar19 = param_1;
                do {
                  uVar8 = (uint)((int)pcVar19 - (int)param_1) >> 2;
                  uVar11 = FUN_001017e0(*(undefined4 *)(pcVar19 + 0x38),uVar6,uVar8,iVar5,1,1);
                  iVar9 = FUN_00103700(local_90 + 0x10,uVar11,iVar5,1);
                  *(uint *)(param_1 + 0x2440) = *(uint *)(param_1 + 0x2440) ^ iVar9 + iVar5;
                  local_58 = FUN_001017e0(iVar9,uVar6,uVar8,iVar5,0,1);
                  if (uVar23 < 5) {
                    uVar8 = uVar23;
                    if (uVar23 != 0) goto LAB_00102fa2;
                  }
                  else {
                    uVar8 = 4;
LAB_00102fa2:
                    if (uVar8 != 0) {
                      uVar12 = 0;
                      do {
                        uVar18 = (ulong)uVar12;
                        uVar12 = uVar12 + 1;
                        pcVar19[uVar18 + 0x1018] = *(char *)((long)&local_58 + uVar18);
                      } while (uVar12 < uVar8);
                    }
                  }
                  pcVar19 = pcVar19 + 4;
                  uVar23 = uVar23 - 4;
                } while (pcVar19 != param_1 + (ulong)(local_a0 - 4) + 4);
              }
            }
            else {
              memset(param_1 + 0x1010,0xff,0x1008);
              iVar5 = *(int *)(param_1 + 0x2434);
              param_1[0x1010] = -0x5b;
              param_1[0x1011] = -0x1b;
              param_1[0x1012] = '\0';
              param_1[0x1013] = '\0';
              param_1[0x1014] = '\0';
              param_1[0x1015] = '\0';
              param_1[0x1016] = '\0';
              param_1[0x1017] = '\0';
              param_1[0x2430] = '\b';
              param_1[0x2431] = '\0';
              param_1[0x2432] = '\0';
              param_1[0x2433] = '\0';
              if (iVar5 == 0) {
                iVar5 = *(int *)(param_1 + 0x242c) + 8;
              }
              *(int *)(param_1 + 0x2424) = iVar5;
            }
            goto LAB_001026cb;
          }
        }
      }
      memset(param_1 + 0x1010,0xff,0x1008);
      iVar5 = *(int *)(param_1 + 0x2434);
      param_1[0x1010] = -0x5b;
      param_1[0x1011] = -0x1b;
      param_1[0x1012] = '\0';
      param_1[0x1013] = '\0';
      param_1[0x1014] = '\0';
      param_1[0x1015] = '\0';
      param_1[0x1016] = '\0';
      param_1[0x1017] = '\0';
      param_1[0x2430] = '\b';
      param_1[0x2431] = '\0';
      param_1[0x2432] = '\0';
      param_1[0x2433] = '\0';
    }
    else {
      if (cVar4 == '\x01') {
        pcVar19 = param_1 + 0x1010;
        if (uVar1 == 0) {
          pcVar17 = param_1 + 0x2090;
          uVar8 = 0;
          do {
            if (*pcVar17 == '\0') {
              lVar20 = (ulong)uVar8 * 0x80;
              cVar4 = FUN_00101bf0(param_1 + lVar20 + 0x2020);
              if (cVar4 == '\0') {
                memset(pcVar19,0xff,0x1008);
                iVar5 = *(int *)(param_1 + 0x2434);
                param_1[0x1010] = -0x5b;
                param_1[0x1011] = -0x19;
                param_1[0x1012] = '\0';
                param_1[0x1013] = '\0';
                param_1[0x1014] = '\0';
                param_1[0x1015] = '\0';
                param_1[0x1016] = '\0';
                param_1[0x1017] = '\0';
                param_1[0x2430] = '\b';
                param_1[0x2431] = '\0';
                param_1[0x2432] = '\0';
                param_1[0x2433] = '\0';
                if (iVar5 == 0) {
                  iVar5 = *(int *)(param_1 + 0x242c) + 8;
                }
                *(int *)(param_1 + 0x2424) = iVar5;
              }
              else {
                param_1[lVar20 + 0x2090] = '\x01';
                iVar5 = *(int *)(param_1 + 0x2438) + 1;
                *(int *)(param_1 + 0x2438) = iVar5;
                *(int *)(param_1 + lVar20 + 0x2020) = iVar5;
                memset(pcVar19,0xff,0x1008);
                iVar9 = *(int *)(param_1 + 0x2434);
                param_1[0x1010] = -0x5b;
                param_1[0x1011] = '\0';
                param_1[0x1012] = '\x04';
                param_1[0x1013] = '\0';
                param_1[0x1014] = '\0';
                param_1[0x1015] = '\0';
                param_1[0x1016] = '\0';
                param_1[0x1017] = '\0';
                param_1[0x2430] = '\f';
                param_1[0x2431] = '\0';
                param_1[0x2432] = '\0';
                param_1[0x2433] = '\0';
                if (iVar9 == 0) {
                  iVar9 = *(int *)(param_1 + 0x242c) + 0xc;
                }
                *(int *)(param_1 + 0x1018) = iVar5;
                *(int *)(param_1 + 0x2424) = iVar9;
              }
              goto LAB_001026cb;
            }
            uVar8 = uVar8 + 1;
            pcVar17 = pcVar17 + 0x80;
          } while (uVar8 != 8);
          memset(pcVar19,0xff,0x1008);
          iVar5 = *(int *)(param_1 + 0x2434);
          param_1[0x1010] = -0x5b;
          param_1[0x1011] = -0x1a;
          param_1[0x1012] = '\0';
          param_1[0x1013] = '\0';
          param_1[0x1014] = '\0';
          param_1[0x1015] = '\0';
          param_1[0x1016] = '\0';
          param_1[0x1017] = '\0';
          param_1[0x2430] = '\b';
          param_1[0x2431] = '\0';
          param_1[0x2432] = '\0';
          param_1[0x2433] = '\0';
        }
        else {
          memset(pcVar19,0xff,0x1008);
          iVar5 = *(int *)(param_1 + 0x2434);
          param_1[0x1010] = -0x5b;
          param_1[0x1011] = -0x1d;
          param_1[0x1012] = '\0';
          param_1[0x1013] = '\0';
          param_1[0x1014] = '\0';
          param_1[0x1015] = '\0';
          param_1[0x1016] = '\0';
          param_1[0x1017] = '\0';
          param_1[0x2430] = '\b';
          param_1[0x2431] = '\0';
          param_1[0x2432] = '\0';
          param_1[0x2433] = '\0';
        }
        goto joined_r0x00102ba0;
      }
      memset(param_1 + 0x1010,0xff,0x1008);
      iVar5 = *(int *)(param_1 + 0x2434);
      param_1[0x1010] = -0x5b;
      param_1[0x1011] = -0x1e;
      param_1[0x1012] = '\0';
      param_1[0x1013] = '\0';
      param_1[0x1014] = '\0';
      param_1[0x1015] = '\0';
      param_1[0x1016] = '\0';
      param_1[0x1017] = '\0';
      param_1[0x2430] = '\b';
      param_1[0x2431] = '\0';
      param_1[0x2432] = '\0';
      param_1[0x2433] = '\0';
    }
  }
  else {
    memset(param_1 + 0x1010,0xff,0x1008);
    iVar5 = *(int *)(param_1 + 0x2434);
    param_1[0x1010] = -0x5b;
    param_1[0x1011] = -0x1f;
    param_1[0x1012] = '\0';
    param_1[0x1013] = '\0';
    param_1[0x1014] = '\0';
    param_1[0x1015] = '\0';
    param_1[0x1016] = '\0';
    param_1[0x1017] = '\0';
    param_1[0x2430] = '\b';
    param_1[0x2431] = '\0';
    param_1[0x2432] = '\0';
    param_1[0x2433] = '\0';
  }
  if (iVar5 == 0) {
    iVar5 = *(int *)(param_1 + 0x242c) + 8;
  }
  *(int *)(param_1 + 0x2424) = iVar5;
LAB_001026cb:
  if (local_40 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00103040 @ 00103040 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
ulong FUN_00103040(long param_1,undefined1 param_2)

{
  ushort uVar1;
  int iVar2;
  ulong uVar3;
  uint uVar4;
  uint uVar5;
  
  if (param_1 == 0) {
    return 0xffffffff;
  }
  uVar4 = *(uint *)(param_1 + 0x2420);
  uVar3 = (ulong)uVar4;
  if (uVar4 < *(uint *)(param_1 + 0x2424)) {
    if (0xf < uVar4) goto LAB_00103090;
LAB_00103066:
    *(undefined1 *)(param_1 + uVar3) = param_2;
    if (uVar4 == 0xf) {
      uVar1 = *(ushort *)(param_1 + 2);
      uVar4 = *(uint *)(param_1 + 0xc);
      if ((uVar1 + 0x18 <= uVar4) && (uVar4 < 0x2005)) {
        *(uint *)(param_1 + 0x2434) = uVar4;
      }
      if (uVar1 < 0x1001) {
        iVar2 = uVar1 + 0x10;
        *(int *)(param_1 + 0x2428) = iVar2;
        *(int *)(param_1 + 0x242c) = iVar2;
        *(int *)(param_1 + 0x2424) = iVar2;
        if (uVar1 == 0) {
          FUN_001025e0(param_1);
          uVar3 = (ulong)*(uint *)(param_1 + 0x2420);
        }
      }
      else {
        memset((void *)(param_1 + 0x1010),0xff,0x1008);
        *(undefined8 *)(param_1 + 0x242c) = 0x800000010;
        iVar2 = *(int *)(param_1 + 0x2434);
        *(undefined8 *)(param_1 + 0x1010) = 0xe3a5;
        if (iVar2 == 0) {
          iVar2 = 0x18;
        }
        *(int *)(param_1 + 0x2424) = iVar2;
      }
    }
  }
  else {
    FUN_00101ad0();
    uVar4 = *(uint *)(param_1 + 0x2420);
    uVar3 = (ulong)uVar4;
    if (uVar4 < 0x10) goto LAB_00103066;
LAB_00103090:
    uVar4 = *(uint *)(param_1 + 0x2428);
    uVar5 = (uint)uVar3;
    if (uVar5 < uVar4) {
      *(undefined1 *)(param_1 + 0x10 + (ulong)(uVar5 - 0x10)) = param_2;
      uVar3 = 0xffffffff;
      if (uVar4 - 1 == uVar5) {
        FUN_001025e0(param_1);
        uVar3 = 0xff;
        uVar5 = *(uint *)(param_1 + 0x2420);
      }
      goto LAB_00103078;
    }
    if ((*(uint *)(param_1 + 0x242c) <= uVar5) &&
       (uVar4 = uVar5 - *(uint *)(param_1 + 0x242c), uVar4 < *(uint *)(param_1 + 0x2430))) {
      uVar3 = (ulong)*(byte *)(param_1 + 0x1010 + (ulong)uVar4);
      goto LAB_00103078;
    }
  }
  uVar5 = (uint)uVar3;
  uVar3 = 0xffffffff;
LAB_00103078:
  *(uint *)(param_1 + 0x2420) = uVar5 + 1;
  return uVar3;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== spi_tpm_fw_get_api_v1 @ 00103200 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined * spi_tpm_fw_get_api_v1(int param_1)

{
  undefined *puVar1;
  
  puVar1 = &DAT_00105d20;
  if (param_1 != 1) {
    puVar1 = (undefined *)0x0;
  }
  return puVar1;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00103220 @ 00103220 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined8 FUN_00103220(undefined8 *param_1)

{
  return *param_1;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00103230 @ 00103230 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined1  [16] FUN_00103230(ulong param_1,ulong param_2,ulong param_3)

{
  undefined1 auVar1 [16];
  undefined1 auVar2 [16];
  undefined1 auVar3 [16];
  undefined1 auVar4 [16];
  undefined1 auVar5 [16];
  ulong uVar6;
  ulong uVar7;
  ulong uVar8;
  ulong uVar9;
  bool bVar10;
  undefined1 auVar11 [16];
  
  auVar1._8_8_ = 0;
  auVar1._0_8_ = param_3;
  auVar3._8_8_ = 0;
  auVar3._0_8_ = param_1;
  uVar6 = SUB168(auVar1 * auVar3,0);
  auVar5._8_8_ = 0;
  auVar5._0_8_ = SUB168(auVar1 * auVar3,8);
  auVar2._8_8_ = 0;
  auVar2._0_8_ = param_3;
  auVar4._8_8_ = 0;
  auVar4._0_8_ = param_2;
  auVar5 = auVar2 * auVar4 + auVar5;
  uVar7 = auVar5._0_8_;
  uVar8 = uVar7 >> 0x3f | auVar5._8_8_ << 1;
  uVar9 = uVar6 + uVar8;
  uVar8 = (uVar7 & 0x7fffffffffffffff) + (ulong)CARRY8(uVar6,uVar8);
  uVar7 = -((long)uVar8 >> 0x3f);
  uVar6 = uVar9 + uVar7;
  uVar7 = (uVar8 & 0x7fffffffffffffff) + (ulong)CARRY8(uVar9,uVar7);
  if (0x7fffffffffffffff < uVar7 || 0x7fffffffffffffff - uVar7 < (ulong)(0xfffffffffffffffe < uVar6)
     ) {
    bVar10 = 0xfffffffffffffffe < uVar6;
    uVar6 = uVar6 + 1;
    uVar7 = uVar7 + 0x8000000000000000 + (ulong)bVar10;
  }
  auVar11._8_8_ = uVar7;
  auVar11._0_8_ = uVar6;
  return auVar11;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_001032f0 @ 001032f0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
undefined1  [16] FUN_001032f0(ulong param_1,ulong param_2)

{
  ulong uVar1;
  ulong uVar2;
  ulong uVar3;
  undefined8 uVar4;
  undefined1 auVar5 [16];
  undefined1 auVar6 [16];
  
  param_2 = (param_1 & 0xffffffff) * -0x2917014799a6026d ^ param_2;
  uVar1 = param_2 + 0x9e3779b97f4a7c15;
  uVar1 = (uVar1 >> 0x1e ^ uVar1) * -0x40a7b892e31b1a47;
  uVar2 = (uVar1 >> 0x1b ^ uVar1) * -0x6b2fb644ecceee15;
  uVar1 = (param_2 ^ 0xa5a3564e27f8862f) + 0x9e3779b97f4a7c15;
  uVar1 = (uVar1 >> 0x1e ^ uVar1) * -0x40a7b892e31b1a47;
  uVar3 = uVar2 ^ uVar2 >> 0x1f;
  uVar1 = (uVar1 >> 0x1b ^ uVar1) * -0x6b2fb644ecceee15;
  uVar1 = (uVar1 >> 0x1f ^ uVar1) & 0x7fffffffffffffff;
  if (uVar3 == 0xffffffffffffffff) {
    uVar4 = 0xffffffffffffffff;
    if (uVar1 == 0x7fffffffffffffff) {
      uVar1 = 0;
      uVar4 = 1;
    }
    auVar6._8_8_ = uVar1;
    auVar6._0_8_ = uVar4;
    return auVar6;
  }
  if (uVar2 - (uVar2 >> 0x1f) == 0) {
    uVar3 = (ulong)(uVar1 == 0);
  }
  auVar5._8_8_ = uVar1;
  auVar5._0_8_ = uVar3;
  return auVar5;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_001033d0 @ 001033d0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
uint FUN_001033d0(ushort param_1,ulong param_2,ulong param_3,uint param_4)

{
  ulong uVar1;
  ulong uVar2;
  
  uVar1 = ((param_3 << 0x11 | param_3 >> 0x2f) ^ param_2 ^ (ulong)param_1 * -0x2917014799a6026d ^
           (ulong)param_4 * -0x5a5ca9b1d80779d1 ^ 0x62696c696e2d7221) + 0x9e3779b97f4a7c15;
  uVar1 = (uVar1 >> 0x1e ^ uVar1) * -0x40a7b892e31b1a47;
  uVar1 = (uVar1 >> 0x1b ^ uVar1) * -0x6b2fb644ecceee15;
  uVar1 = ((param_2 << 0x1d | param_2 >> 0x23) ^ param_3 ^ uVar1 ^ uVar1 >> 0x1f) +
          0x9e3779b97f4a7c15;
  uVar1 = (uVar1 >> 0x1e ^ uVar1) * -0x40a7b892e31b1a47;
  uVar1 = (uVar1 >> 0x1b ^ uVar1) * -0x6b2fb644ecceee15;
  uVar2 = uVar1 >> 0x1f ^ uVar1;
  return (uint)(uVar2 >> 0x10) ^ (uint)(uVar2 >> 0x20) ^ (uint)uVar2 ^ (uint)(ushort)(uVar1 >> 0x30)
  ;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_001034a0 @ 001034a0 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_001034a0(undefined1 (*param_1) [16],long param_2)

{
  byte bVar1;
  ulong uVar2;
  ulong uVar3;
  undefined1 *puVar4;
  undefined1 *puVar5;
  ulong uVar6;
  ulong uVar7;
  ulong *puVar8;
  long lVar9;
  long lVar10;
  long in_FS_OFFSET;
  undefined1 auVar11 [16];
  ulong local_68;
  ulong uStack_60;
  undefined1 local_58 [16];
  undefined1 local_48 [16];
  undefined1 local_38 [8];
  long local_30;
  
  uVar6 = 1;
  lVar10 = -0x40a7b892e31b1a47;
  lVar9 = -0x6b2fb644ecceee15;
  puVar8 = &local_68;
  local_30 = *(long *)(in_FS_OFFSET + 0x28);
  local_58 = (undefined1  [16])0x0;
  local_48 = (undefined1  [16])0x0;
  *param_1 = (undefined1  [16])0x0;
  param_1[1] = (undefined1  [16])0x0;
  param_1[2] = (undefined1  [16])0x0;
  param_1[3] = (undefined1  [16])0x0;
  param_1[4] = (undefined1  [16])0x0;
  param_1[5] = (undefined1  [16])0x0;
  uVar2 = FUN_00103220(param_2,param_2,&local_68);
  auVar11 = FUN_00103220(param_2 + 8);
  local_68 = uVar2;
  if (uVar2 == 0) {
    local_68 = uVar6;
  }
  uStack_60 = auVar11._0_8_;
  if (auVar11._0_8_ == 0) {
    uStack_60 = uVar6;
  }
  uVar6 = (uStack_60 << 0x17 | uStack_60 >> 0x29) ^ local_68 ^ 0x62696c696e2d7421;
  uVar2 = 0;
  while( true ) {
    uVar6 = (uVar2 ^ uStack_60 ^ uVar6) + 0x9e3779b97f4a7c15;
    uVar6 = (uVar6 >> 0x1e ^ uVar6) * lVar10;
    uVar6 = (uVar6 >> 0x1b ^ uVar6) * lVar9;
    uVar6 = uVar6 >> 0x1f ^ uVar6;
    bVar1 = ('\a' - auVar11[8]) + (char)puVar8 & 0x3f;
    uVar3 = ((uStack_60 << bVar1 | uStack_60 >> 0x40 - bVar1) ^ uVar6 ^ local_68) +
            0x9e3779b97f4a7c15;
    uVar3 = (uVar3 ^ uVar3 >> 0x1e) * lVar10;
    uVar7 = (uVar3 >> 0x1b ^ uVar3) * lVar9;
    uVar3 = uVar7 >> 0x1f ^ uVar7;
    *(char *)((long)puVar8 + 0x10) = (char)uVar3;
    *(char *)((long)puVar8 + 0x11) = (char)(uVar3 >> 8);
    *(char *)((long)puVar8 + 0x12) = (char)(uVar3 >> 0x10);
    *(char *)((long)puVar8 + 0x14) = (char)(uVar3 >> 0x20);
    *(char *)((long)puVar8 + 0x13) = (char)(uVar3 >> 0x18);
    *(char *)((long)puVar8 + 0x15) = (char)(uVar7 >> 0x28);
    *(char *)((long)puVar8 + 0x16) = (char)(uVar7 >> 0x30);
    *(char *)((long)puVar8 + 0x17) = (char)(uVar7 >> 0x38);
    if (uVar2 + 0xf1bbcdcbfa53e0a8 == 0xc6ef372fe94f82a0) break;
    puVar8 = (ulong *)((long)puVar8 + 8);
    uVar2 = uVar2 + 0xf1bbcdcbfa53e0a8;
  }
  *(ulong *)*param_1 = local_68;
  *(ulong *)(*param_1 + 8) = uStack_60;
  *(undefined8 *)param_1[1] = local_58._0_8_;
  *(undefined8 *)(param_1[1] + 8) = local_58._8_8_;
  *(undefined8 *)param_1[2] = local_48._0_8_;
  *(undefined8 *)(param_1[2] + 8) = local_48._8_8_;
  puVar4 = auVar11._8_8_;
  do {
    puVar5 = puVar4 + 1;
    *puVar4 = 0;
    puVar4 = puVar5;
  } while (puVar5 != local_38);
  if (local_30 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00103690 @ 00103690 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void FUN_00103690(undefined8 *param_1,undefined8 *param_2)

{
  undefined8 *puVar1;
  undefined1 *puVar2;
  long in_FS_OFFSET;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined8 local_38;
  undefined8 uStack_30;
  undefined8 local_28;
  undefined8 uStack_20;
  undefined1 local_18 [8];
  long local_10;
  
  local_48 = *param_1;
  uStack_40 = param_1[1];
  local_38 = param_1[2];
  uStack_30 = param_1[3];
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_28 = param_1[4];
  uStack_20 = param_1[5];
  *param_2 = local_38;
  param_2[1] = uStack_30;
  param_2[2] = local_28;
  param_2[3] = uStack_20;
  puVar1 = &local_48;
  do {
    puVar2 = (undefined1 *)((long)puVar1 + 1);
    *(undefined1 *)puVar1 = 0;
    puVar1 = (undefined8 *)puVar2;
  } while (puVar2 != local_18);
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00103700 @ 00103700 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
ulong FUN_00103700(undefined8 *param_1,ulong param_2,uint param_3,char param_4)

{
  undefined8 uVar1;
  uint uVar2;
  undefined8 *puVar3;
  undefined1 *puVar4;
  uint uVar5;
  ulong uVar6;
  undefined8 uVar7;
  ulong uVar8;
  long in_FS_OFFSET;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 uStack_40;
  undefined8 local_38;
  undefined8 uStack_30;
  undefined1 local_28 [8];
  long local_20;
  
  uVar1 = *param_1;
  uVar7 = param_1[1];
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  uVar6 = (ulong)param_3;
  local_48 = param_1[2];
  uStack_40 = param_1[3];
  local_38 = param_1[4];
  uStack_30 = param_1[5];
  local_58 = uVar1;
  uStack_50 = uVar7;
  if (param_4 == '\0') {
    if (param_3 != 0) {
      param_2 = param_2 & 0xffffffff;
      uVar8 = 0;
      do {
        uVar5 = (uint)param_2;
        uVar2 = (uint)uVar8;
        uVar8 = (ulong)(uVar2 + 1);
        uVar2 = FUN_001033d0(param_2 >> 0x10,uVar1,uVar7,uVar2 & 3);
        param_2 = (ulong)((uVar2 ^ uVar5) << 0x10 | (uint)(param_2 >> 0x10));
      } while ((int)uVar6 != (int)uVar8);
      goto LAB_001037fc;
    }
  }
  else if (param_3 != 0) {
    param_2 = param_2 & 0xffffffff;
    do {
      param_3 = param_3 - 1;
      uVar2 = FUN_001033d0(param_2 & 0xffff,uVar1,uVar7,param_3 & 3);
      param_2 = (ulong)((int)param_2 << 0x10 | (uVar2 ^ (uint)(param_2 >> 0x10) & 0xffff) & 0xffff);
    } while (param_3 != 0);
    goto LAB_001037fc;
  }
  param_2 = param_2 & 0xffffffff;
LAB_001037fc:
  puVar3 = &local_58;
  do {
    puVar4 = (undefined1 *)((long)puVar3 + 1);
    *(undefined1 *)puVar3 = 0;
    puVar3 = (undefined8 *)puVar4;
  } while (puVar4 != local_28);
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return param_2;
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== FUN_00103850 @ 00103850 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
uint FUN_00103850(undefined8 *param_1,uint param_2)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  undefined8 uVar4;
  ulong uVar5;
  ulong uVar6;
  ulong uVar7;
  ulong uVar8;
  long in_FS_OFFSET;
  bool bVar9;
  undefined1 auVar10 [16];
  undefined1 auVar11 [16];
  undefined1 auVar12 [16];
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  long local_40;
  
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  auVar10 = FUN_001032f0(param_2,0x62696c696e2d6121);
  auVar11 = FUN_001032f0(param_2,0x62696c696e2d6221);
  uVar4 = auVar11._8_8_;
  auVar12 = FUN_001032f0(param_2,0x62696c696e2d6321);
  local_78 = *param_1;
  uVar1 = param_1[1];
  local_68 = param_1[2];
  uStack_60 = param_1[3];
  local_58 = param_1[4];
  uStack_50 = param_1[5];
  uStack_70 = uVar1;
  auVar11 = FUN_00103230(auVar11._0_8_,uVar4,uVar1);
  uVar4 = local_78;
  auVar10 = FUN_00103230(auVar10._0_8_,auVar10._8_8_,local_78);
  uVar5 = SUB168(auVar11 + auVar10,0);
  uVar8 = SUB168(auVar11 + auVar10,8);
  uVar6 = -((long)uVar8 >> 0x3f);
  uVar7 = uVar6 + uVar5;
  uVar5 = (uVar8 & 0x7fffffffffffffff) + (ulong)CARRY8(uVar6,uVar5);
  if (0x7fffffffffffffff < uVar5 || 0x7fffffffffffffff - uVar5 < (ulong)(0xfffffffffffffffe < uVar7)
     ) {
    bVar9 = 0xfffffffffffffffe < uVar7;
    uVar7 = uVar7 + 1;
    uVar5 = uVar5 + 0x8000000000000000 + (ulong)bVar9;
  }
  auVar10._8_8_ = uVar5;
  auVar10._0_8_ = uVar7;
  auVar11 = FUN_00103230(auVar12._0_8_,auVar12._8_8_,uVar4);
  auVar11 = FUN_00103230(auVar11._0_8_,auVar11._8_8_,uVar1);
  uVar6 = SUB168(auVar11 + auVar10,0);
  uVar8 = SUB168(auVar11 + auVar10,8);
  uVar7 = -((long)uVar8 >> 0x3f);
  uVar5 = uVar6 + uVar7;
  uVar6 = (uVar8 & 0x7fffffffffffffff) + (ulong)CARRY8(uVar6,uVar7);
  if (0x7fffffffffffffff < uVar6 || 0x7fffffffffffffff - uVar6 < (ulong)(0xfffffffffffffffe < uVar5)
     ) {
    uVar6 = uVar6 + 0x8000000000000000 + (ulong)(0xfffffffffffffffe < uVar5);
  }
  uVar5 = ((ulong)param_2 ^ 0x62696c696e2d7274) + 0x9e3779b97f4a7c15;
  uVar5 = (uVar5 ^ uVar5 >> 0x1e) * -0x40a7b892e31b1a47;
  uVar5 = (uVar5 >> 0x1b ^ uVar5) * -0x6b2fb644ecceee15;
  puVar2 = &local_78;
  do {
    puVar3 = (undefined8 *)((long)puVar2 + 1);
    *(undefined1 *)puVar2 = 0;
    puVar2 = puVar3;
  } while (puVar3 != &local_48);
  if (local_40 == *(long *)(in_FS_OFFSET + 0x28)) {
    return (uint)(uVar5 >> 0x1f) ^ (uint)uVar5 ^ (uint)(uVar6 >> 0x36);
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

 (GhidraScript)  
INFO  DecompileAll.java> 
/* ===== _DT_FINI @ 00103ac8 ===== */ (GhidraScript)  
INFO  DecompileAll.java> 
void _DT_FINI(void)

{
  return;
}

 (GhidraScript)  
INFO  ANALYZING changes made by post scripts: file:///home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so (HeadlessAnalyzer)  
INFO  REPORT: Post-analysis succeeded for file: file:///home/sh4d0w/HitconCTF/reversing/SPI_TPM_Free_Trial/spi-tpm-rev/src/libspi_tpm_firmware.so (HeadlessAnalyzer)  
INFO  /libspi_tpm_firmware.so: file created (sh4d0w) (LocalFileSystem)  
INFO  REPORT: Save succeeded for: /libspi_tpm_firmware.so (fwproj:/libspi_tpm_firmware.so) (HeadlessAnalyzer)  
INFO  REPORT: Import succeeded (HeadlessAnalyzer)  
