  ! Fortran 90 implementation of 
program euler 
  implicit none
  integer, parameter :: n = 10
  integer :: s,f 
  do i = 1, n
     f = call fact(n)
     s = s + (1 / f) 
  end do  
end program 

integer function fact(n)
  implicit none 
  integer :: n,f

  do i = 1, n 
     f = f * i  
  end do 
  
  fact = f
end function fact

