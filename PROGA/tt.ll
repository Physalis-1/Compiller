; ModuleID = "module"
target triple = "i686-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare double @"printfloat"(i8* %".1", ...) 

define void @"__init"() 
{
entry:
  br label %"exit"
exit:
  ret void
}

define void @"__init_main"() 
{
entry:
  %".2" = bitcast [5 x i8]* @"fstr" to i8*
  %".3" = call double (i8*, ...) @"printfloat"(i8* %".2", double 0x4072c00000000000)
  br label %"exit"
exit:
  ret void
}

@"fstr" = internal constant [5 x i8] c"%f \0a\00"