﻿using Questionnaires.Question;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Questionnaires.Renderer
{
    interface IRenderer
    {
        void AddQuestion(QL.AST.Question question);
        void SetValue(string name, Questionnaires.Value.IValue value);
        void SetVisibility(string name, bool visibile);
        void SetWindowTitle(string title);
    }
}
