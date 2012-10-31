/*
Adapted from python-udunits: https://code.google.com/p/python-udunits/

Copyright (C) 2011  Constantine Khroulev

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

===

Author: Christopher Mueller
Copyright (C) UC Regents 2012
/*

/* -*- mode: c++ -*- */
%module udunits2_c

%{
#include <udunits.h>
%}

%include cstring.i
%include typemaps.i

%apply int * OUTPUT { int * };
%apply double * OUTPUT { double * second };
%apply double * OUTPUT { double * resolution };

 /* Avoid the clash with a Python keyword. */
%rename("pow") "ut_raise";

/* Remove the "ut_" prefix */
%rename("%(strip:[ut_])s") "";

%newobject ut_clone;
%newobject ut_divide;
%newobject ut_get_converter;
%newobject ut_get_dimensionless_unit_one;
//%newobject ut_get_system;       // does not allocate a new system
%newobject ut_get_unit_by_name;
%newobject ut_get_unit_by_symbol;
%newobject ut_invert;
%newobject ut_log;
%newobject ut_multiply;
%newobject ut_new_base_unit;
%newobject ut_new_dimensionless_unit;
%newobject ut_new_system;
%newobject ut_offset;
%newobject ut_offset_by_time;
%newobject ut_parse;
%newobject ut_raise;
%newobject ut_read_xml;
%newobject ut_root;
%newobject ut_scale;

// udunits2.h
%cstring_output_maxsize(char* buffer, size_t buffer_size);
int ut_format(const ut_unit* const unit, char* buffer, size_t buffer_size, unsigned opts);

// Pretend that ut_unit and ut_system are empty: SWIG refuses to extend a
// struct or a union with an incomplete type. :-(
typedef union ut_unit {} ut_unit;
%extend ut_unit { ~ut_unit() { ut_free($self); } };

typedef struct ut_system {} ut_system;
%extend ut_system { ~ut_system() { ut_free_system($self); } };

%ignore ut_write_to_stderr;
%ignore ut_error_message_handler;
%ignore ut_set_error_message_handler;
%ignore ut_ignore;
%ignore ut_trim;
%ignore ut_visitor;
%ignore ut_accept_visitor;
%ignore ut_format;
%ignore ut_unit;
%ignore ut_system;
%ignore ut_free;
%ignore ut_free_system;
%include <udunits2.h>

 // converter.h

%newobject cv_get_trivial;
%newobject cv_get_inverse;
%newobject cv_get_scale;
%newobject cv_get_offset;
%newobject cv_get_galilean;
%newobject cv_get_log;
%newobject cv_get_pow;
%newobject cv_combine;

// See the comment about ut_unit and ut_system above.
typedef union cv_converter {} cv_converter;
%extend cv_converter { ~cv_converter() { cv_free($self); } };

%cstring_output_maxsize(char* const buffer, size_t buffer_size);
int cv_get_expression(const cv_converter* const conv, char* const buffer, size_t buffer_size,
                      const char* const variable);

%ignore cv_free;
%ignore cv_converter;
%ignore cv_convert_float;
%ignore cv_convert_floats;
%ignore cv_get_expression;
%include <converter.h>

%init %{
	ut_set_error_message_handler(ut_ignore);
%}