﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Questionnaires.QLS.AST.Widgets
{
    public abstract class Widget : INode
    {
        public virtual Questionnaires.Renderer.Widgets.QuestionWidget CreateWidget(Types.IType type)
        {
            throw new NotSupportedException();
        }

        public virtual Questionnaires.Renderer.Widgets.QuestionWidget CreateWidget(Types.BooleanType type)
        {
            throw new NotSupportedException();
        }

        public virtual Questionnaires.Renderer.Widgets.QuestionWidget CreateWidget(Types.StringType type)
        {
            throw new NotSupportedException();
        }

        public virtual Questionnaires.Renderer.Widgets.QuestionWidget CreateWidget(Types.IntegerType type)
        {
            throw new NotSupportedException();
        }

        public virtual Questionnaires.Renderer.Widgets.QuestionWidget CreateWidget(Types.MoneyType type)
        {
            throw new NotSupportedException();
        }
    }
}